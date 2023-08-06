"""FPGA Sensors representations."""
from __future__ import annotations
from abc import ABC
from enum import Enum
from typing import Any

from fpga_i2c_bridge import UnknownDeviceTypeError, I2CShutter
from fpga_i2c_bridge.util import Logger


class I2CSensorType(Enum):
    """Enumeration for all sensor types."""
    BUTTON = 0x01
    TOGGLE = 0x02
    DIMMER_CYCLE = 0x03
    RGB_CYCLE = 0x04
    SHUTTER_CTRL = 0x05


class I2CSensor(ABC):
    """Base class for representing a sensor."""
    def __init__(self, bridge: 'I2CBridge', sensor_id: int, sensor_type: I2CSensorType):
        self.bridge = bridge
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.state = None
        self.logger = Logger.get_logger(self)

    @staticmethod
    def create(bridge: 'I2CBridge', sensor_id: int, sensor_type: I2CSensorType) -> I2CSensor:
        """
        Factory method for creating a sensor object based on the supplied device type.
        If the type of sensor is unknown, this raises an UnknownDeviceTypeError.
        :param bridge: Bridge this appliance belongs to
        :param sensor_id: Sensor's device ID
        :param sensor_type: Sensor's raw type
        :return: Sensor object instance
        """
        try:
            return _INPUT_CONSTRUCTORS[sensor_type](bridge=bridge, sensor_id=sensor_id, sensor_type=sensor_type)

        except KeyError:
            raise UnknownDeviceTypeError(sensor_type.value)

    def on_input(self, input_data: int) -> None:
        """
        Passes input event data to this sensor. Used during polling.
        :param input_data: Input event data
        """
        raise NotImplementedError

    def __str__(self):
        return f"ID {self.sensor_id}"


class I2CBinarySensor(I2CSensor, ABC):
    """Abstract class for binary sensors (Buttons, Toggles and Cyclers)."""
    def __init__(self, *args, **kwargs):
        super(I2CBinarySensor, self).__init__(*args, **kwargs)

        self._event_callbacks = {}

    def register_event_handler(self):
        """
        Decorator that registers the following function as a callback that will be called when this sensor emits that
        it has been (de)pressed.
        The function must take one parameter, which will contain the Input event data.
        :return: Decorator
        """
        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._event_callbacks[function.__name__] = wrapper

        return decorator

    def _fire_event(self, event_data: int) -> None:
        for func in self._event_callbacks.values():
            func(event_data)


class I2CPassthroughSensor(I2CBinarySensor):
    """Representation for a sensor that passes through its input (Buttons, Toggles)."""
    def __init__(self, *args, **kwargs):
        super(I2CPassthroughSensor, self).__init__(*args, **kwargs)

    def on_input(self, input_data: int) -> None:
        """
        Passes input event data onto this sensor, which it passes through to subscribers.
        :param input_data: Input event data
        """
        self._fire_event(input_data)

    def __str__(self):
        return f"Button ({super().__str__()})"


class I2CCycleButtonSensor(I2CBinarySensor):
    """Representation for a Cycle sensor (Dimmer Cycle, RGB Cycle)."""
    def __init__(self, *args, **kwargs):
        super(I2CCycleButtonSensor, self).__init__(*args, **kwargs)

    def on_input(self, input_data: int) -> None:
        """
        Passes input event data onto this sensor. The data is ignored, and two events (1 and 0) are sent to subscribers
        in short succession.
        :param input_data: Input event data; ignored
        """
        self._fire_event(1)
        self._fire_event(0)

    def __str__(self):
        return f"Button ({super().__str__()})"


class I2CShutterControlSensor(I2CSensor):
    """Representation for a Shutter Control sensor."""
    def __init__(self, *args, **kwargs):
        super(I2CShutterControlSensor, self).__init__(*args, **kwargs)

        self._handlers = {
            I2CShutter.State.UP_ONCE: {},
            I2CShutter.State.UP_FULL: {},
            I2CShutter.State.DOWN_ONCE: {},
            I2CShutter.State.DOWN_FULL: {}
        }

    def on_input(self, input_data: int) -> None:
        """
        Passes input event data to this sensor. The value is a valid Shutter state, and the according subscribers are
        notified about the event.
        :param input_data: Input event data (a valid Shutter state)
        """
        try:
            state = I2CShutter.State(input_data)
            self._call_handlers(state)
        except KeyError as e:
            self.logger.error(f"Received unknown shutter control input: {e}")

    def _register_handler(self, handler_type: I2CShutter.State):
        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._handlers[handler_type][function.__name__] = wrapper

        return decorator

    def _call_handlers(self, handler_type: I2CShutter.State):
        for func in self._handlers[handler_type].values():
            func()

    def register_short_up_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every short up press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.UP_ONCE)

    def register_short_down_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every short down press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.DOWN_ONCE)

    def register_full_up_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every long up press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.UP_FULL)

    def register_full_down_handler(self):
        """
        Decorator that registers the following function as a callback that will be called on every long down press
        emitted from the Shutter control.
        The function must not take any parameters.
        :return: Decorator
        """
        return self._register_handler(I2CShutter.State.DOWN_FULL)

    def __str__(self):
        return f"Shutter Control ({super().__str__()})"


_INPUT_CONSTRUCTORS = {
    I2CSensorType.BUTTON: I2CPassthroughSensor,
    I2CSensorType.TOGGLE: I2CPassthroughSensor,
    I2CSensorType.DIMMER_CYCLE: I2CCycleButtonSensor,
    I2CSensorType.RGB_CYCLE: I2CCycleButtonSensor,
    I2CSensorType.SHUTTER_CTRL: I2CShutterControlSensor
}