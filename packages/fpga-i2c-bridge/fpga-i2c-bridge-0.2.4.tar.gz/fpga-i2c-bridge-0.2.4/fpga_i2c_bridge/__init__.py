"""I2C Bridge API. Provides an interface for the FPGA smart home bridge."""

import threading
from time import sleep
from typing import List, Dict

from fpga_i2c_bridge.appliance import I2CGenericBinary, I2CDimmer, I2CRGBDimmer, I2CShutter, I2CAppliance, I2CApplianceType, \
    UnknownDeviceTypeError, InvalidStateError
from fpga_i2c_bridge.sensor import I2CSensor, I2CSensorType
from fpga_i2c_bridge.net.error import I2CException
from fpga_i2c_bridge.net.packet import I2CApplianceStateResponse, I2CInputEventResponse
from fpga_i2c_bridge.util import Logger


class I2CBridge:
    """Represents a FPGA smart home bridge."""
    def __init__(self, i2c_dummy=False, i2c_dummy_appliances: List[int] = None, i2c_dummy_sensors: List[int] = None,
                 i2c_bus=1, i2c_addr=0x3E):
        """The I2C hardware bus to be used."""
        self.bus = i2c_bus

        """The I2C slave address of the FPGA."""
        self.addr = i2c_addr

        if i2c_dummy:
            from fpga_i2c_bridge.i2c_dummy import I2CDummy
            self.i2c = I2CDummy(appliance_types=i2c_dummy_appliances or [4, 3, 2, 1],
                                sensor_types=i2c_dummy_sensors or [5, 4, 3, 2, 1], error_ratio=0.002)
        else:
            from fpga_i2c_bridge.i2c import I2CBusReal
            self.i2c = I2CBusReal(bus=i2c_bus, addr=i2c_addr)

        self.logger = Logger.get_logger(self)

        """The reported version of the FPGA."""
        self.version = None
        self._num_appliances = 0
        self._num_sensors = 0

        self._query_status()

        """Contains all appliances connected to the bridge, indexed by their device IDs."""
        self.appliances: Dict[int, I2CAppliance] = {}

        """Contains all sensors connected to the bridge, indexed by their input device IDs."""
        self.sensors: Dict[int, I2CSensor] = {}

        self._query_devices()

        self.is_polling = False
        self.poll_update_callbacks = {}
        self.poll_delay = 0.5
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()
        self.poll_fail_delay = 2

    def _query_status(self) -> None:
        """Queries status and number of devices from the FPGA."""
        info = self.i2c.get_fpga_status()
        self.logger.info("FPGA Version %08x, %d appliances, %d sensors" %
                         (info.version, info.num_appliances, info.num_sensors))
        self.version = info.version
        self._num_appliances = info.num_appliances
        self._num_sensors = info.num_sensors

    def _query_devices(self) -> None:
        """
        Queries all devices from the FPGA. Device objects are created accordingly and stored inside the devices and
        inputs fields.
        """
        self.logger.info("Scanning for devices...")
        self.appliances = {}

        try:
            for i in range(self._num_appliances):
                dev_type = self.i2c.get_appliance_type(i).device_type
                if dev_type > 0:
                    try:
                        self.appliances[i] = I2CAppliance.create(bridge=self, device_id=i,
                                                                 device_type=I2CApplianceType(dev_type))
                        self.logger.info("Device %02x is a %s" % (i, self.appliances[i]))
                        self.appliances[i].update_state(self.i2c.get_appliance_state(i).device_state)
                    except UnknownDeviceTypeError as e:
                        self.logger.error(f"Couldn't set up device ID {i}: {e}")
                else:
                    self.appliances[i] = None

        except I2CException as e:
            self.logger.warn("I2C error while scanning for devices: %s" % e)

        self.logger.info("Found %d devices" % sum(d is not None for d in self.appliances.values()))
        self.logger.info("Scanning for inputs...")
        self.sensors = {}
        try:
            for i in range(self._num_sensors):
                input_type = self.i2c.get_sensor_type(i).sensor_type
                try:
                    self.sensors[i] = I2CSensor.create(bridge=self, sensor_id=i, sensor_type=I2CSensorType(input_type))
                except UnknownDeviceTypeError as e:
                    self.logger.info(f"Couldn't set up Input ID {i}: {e}")

        except I2CException as e:
            self.logger.warn(f"I2C error while scanning for inputs: {e}")

        self.logger.info("Found %d inputs" % sum(d is not None for d in self.sensors.values()))

    def poll(self) -> None:
        """
        Performs a manual poll request on the FPGA. For any incoming events, the appropriate registered callback
        handlers are called.
        """
        for event in self.i2c.poll():
            try:
                # Device updates
                if isinstance(event, I2CApplianceStateResponse):
                    try:
                        # Update local device state and forward to device handlers
                        self.appliances[event.device_id].update_state(event.device_state)

                        # Call global handlers
                        for func in self.poll_update_callbacks.values():
                            func(self.appliances[event.device_id])

                    except (ValueError, InvalidStateError) as e:
                        self.logger.warning(f"Malformed state update event data, ignoring: {e}")

                # Input events
                elif isinstance(event, I2CInputEventResponse):
                    try:
                        # Send event to input device so that it can call its handlers
                        self.sensors[event.sensor_id].on_input(event.sensor_data)

                    except ValueError as e:
                        self.logger.warning(f"Malformed event data, ignoring: {e}")

            except I2CException as e:
                self.logger.error(f"Failed to forward event: {e}")

    def register_update(self):
        """
        Decorator that registers the following function as a global callback handler for State Update events.
        The callback function must take two parameters: the device that caused the event and the raw state data.
        :return: Decorator for function.
        """
        def decorator(function):
            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                return result

            self.poll_update_callbacks[function.__name__] = wrapper

        return decorator

    def start_polling(self, delay: float = 0.5) -> None:
        """
        Starts automatic polling of the FPGA.
        :param delay: Polling frequency.
        """
        self.poll_delay = delay
        if self.is_polling:
            return

        self.logger.info("Starting auto-polling")
        self.is_polling = True

    def stop_polling(self) -> None:
        """
        Stops automatic polling of the FPGA.
        """
        if not self.is_polling:
            return

        self.logger.info("Stopping auto-polling")
        self.is_polling = False

    def _poll_loop(self) -> None:
        self.logger.info("Starting polling thread")

        try:
            while True:
                try:
                    if self.is_polling:
                        self.poll()

                    sleep(self.poll_delay)
                    self.poll_fail_delay = 1

                except I2CException as e:
                    self.logger.warn(f"Communication failure: {e}")
                    self.logger.info(f"Attempting to resume polling in {self.poll_fail_delay}s")

                    sleep(self.poll_fail_delay)
                    self.poll_fail_delay = min(self.poll_fail_delay + 2, 30)

        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Polling thread: Received exit signal")

        self.logger.info("Closing polling thread")

    def reset(self) -> None:
        """
        Sends a reset signal to the FPGA.
        """
        was_polling = False
        if self.is_polling:
            was_polling = True
            self.stop_polling()

        self.i2c.reset_fpga()
        self._query_devices()

        if was_polling:
            self.start_polling()

    def send_state(self, device_id: int, new_state: int) -> bool:
        """
        Sends a state update request to the device with the specified ID.
        :param device_id: ID of the device to set the new state for.
        :param new_state: Raw new state value.
        :return: True if the state update request succeeded, False otherwise.
        """
        try:
            self.i2c.set_appliance_state(device_id, new_state)
            return True
        except I2CException as e:
            self.logger.warn("Sending device state failed: %s" % e)
            return False

    def __str__(self) -> str:
        return "FPGA Bridge @ I2C Bus %d, Addr 0x%02x" % (self.bus, self.addr)