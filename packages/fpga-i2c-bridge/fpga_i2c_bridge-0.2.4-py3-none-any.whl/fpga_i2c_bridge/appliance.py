"""FPGA appliance representations."""

from enum import Enum
from typing import Any, Tuple, Optional

from fpga_i2c_bridge.util import Logger


class InvalidStateError(BaseException):
    """Exception that gets thrown when an invalid state value has been supplied for an appliance."""
    def __init__(self, device: 'I2CAppliance', state: Any):
        super(InvalidStateError, self).__init__("%s is not a valid state for device %s" % (state, device))


class UnknownDeviceTypeError(BaseException):
    """Exception that gets thrown when a device of an unknown type is attempted to be created."""
    def __init__(self, device_type: int):
        super(UnknownDeviceTypeError, self).__init__(f"Attempted to instantiate device of unknown type {device_type}")


class I2CApplianceType(Enum):
    """Enumeration for all appliance types."""
    BINARY = 0x01
    DIMMER = 0x02
    RGB = 0x03
    SHUTTER = 0x04


class I2CAppliance:
    """Abstract class for representing an appliance."""
    def __init__(self, bridge: 'I2CBridge', device_id: int, device_type: I2CApplianceType,
                 default_state: Optional[Any] = None):
        """The bridge this appliance belongs to."""
        self.bridge = bridge

        """The appliance's device ID."""
        self.device_id = device_id

        """The appliance's device type."""
        self.device_type = device_type

        """The appliance's state."""
        self.state = default_state

        self.logger = Logger.get_logger(self)

        self._update_handlers = {}

    @staticmethod
    def create(bridge: 'I2CBridge', device_id: int, device_type: I2CApplianceType):
        """
        Factory method for creating an appliance object based on the supplied device type.
        If the type of appliance is unknown, this raises an UnknownDeviceTypeError.
        :param bridge: Bridge this appliance belongs to
        :param device_id: Appliance's device ID
        :param device_type: Appliance's raw type
        :return: Appliance object instance
        """
        try:
            return _DEVICE_CLASSES[device_type](bridge=bridge, device_id=device_id)
        except KeyError:
            raise UnknownDeviceTypeError(device_type)

    def _encode_state(self, state: Any) -> int:
        """
        Translates the given state value to its raw 24-bit form.
        :param state: State to translate
        :return: Raw 24-bit state
        """
        raise NotImplementedError

    def _decode_state(self, raw_state: int) -> Any:
        """
        Translates the given raw 24-bit state into a more sensible type.
        :param raw_state: Raw 24-bit state
        :return: Interpreted state value
        """
        raise NotImplementedError

    def set_state(self, new_state: Any) -> None:
        """
        Requests to set the state of this appliance to the given value, which needs to be a valid state value in the
        context of this device.
        :param new_state: New state value to set
        """
        encoded_state = self._encode_state(new_state)
        self.logger.info("Set state to %s (0x%06x)" % (new_state, encoded_state))
        if self.bridge.send_state(self.device_id, encoded_state):
            self.state = new_state

    def update_state(self, new_state: int) -> None:
        """
        Updates its own state. This is done after receiving a State Update event, and will call all state update
        handler callbacks.
        :param new_state: New raw 24-bit state value
        """
        self.state = self._decode_state(new_state)
        self.logger.debug("State update: %s (Raw: %06x)" % (self.state, new_state))

        self._call_update_handlers()

    def register_update_handler(self):
        """
        Decorator that registers the following function as a callback that will be called when this appliance updates
        its own state through a State Update event.
        The function must not take any parameters.
        :return: Decorator
        """
        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)

            self._update_handlers[function.__name__] = wrapper

        return decorator

    def _call_update_handlers(self):
        for func in self._update_handlers.values():
            func()

    def __str__(self):
        return "ID %d" % self.device_id


class I2CGenericBinary(I2CAppliance):
    """Represents a Generic Binary device."""
    def __init__(self, bridge: 'I2CBridge', device_id: int):
        super(I2CGenericBinary, self).__init__(bridge=bridge, device_id=device_id, device_type=I2CApplianceType.BINARY,
                                               default_state=False)

    def _encode_state(self, state: bool) -> int:
        """
        Translates the given state to its raw 24-bit equivalent. This returns 0 for False and 1 for True.
        :param state: Generic Binary state to translate
        :return: 0 for False, or 1 for True
        """
        return int(state)

    def _decode_state(self, raw_state: int) -> bool:
        """
        Translates the given raw 24-bit state to a Boolean value. This returns False for 0, and True otherwise.
        :param raw_state: Raw 24-bit state value
        :return: False for 0, True otherwise
        """
        return bool(raw_state)

    def turn_on(self) -> None:
        """
        Turns on the Generic Binary appliance.
        """
        self.set_state(True)

    def turn_off(self) -> None:
        """
        Turns off the Generic Binary appliance.
        """
        self.set_state(False)

    def toggle(self) -> None:
        """
        Toggles the state of the Generic Binary appliance.
        """
        self.set_state(not self.state)

    def __str__(self):
        return "Switch (%s)" % super().__str__()


class I2CDimmer(I2CAppliance):
    """Represents a Dimmer appliance."""
    def __init__(self, bridge: 'I2CBridge', device_id: int):
        super(I2CDimmer, self).__init__(bridge=bridge, device_id=device_id, device_type=I2CApplianceType.DIMMER,
                                        default_state=0.0)

    def _encode_state(self, state: float) -> int:
        try:
            if 0 <= state <= 1:
                return round(state * 255)

            # Not a valid state otherwise
            raise TypeError

        except TypeError:
            raise InvalidStateError(self, state)

    def _decode_state(self, raw_state: int) -> float:
        return (raw_state % 256) / 255

    def set_brightness(self, brightness: float) -> None:
        """
        Sets the brightness of this Dimmer. It is expressed through a float value between 0 and 1 inclusive, with
        0 being off, and 1 being the maximum possible brightness.
        :param brightness: Brightness value as a float between 0 and 1 inclusive
        """
        self.set_state(brightness)

    def __str__(self):
        return "Dimmer (%s)" % super().__str__()


class I2CRGBDimmer(I2CAppliance):
    """Represents a RGB Dimmer appliance."""
    def __init__(self, bridge: 'I2CBridge', device_id: int):
        super(I2CRGBDimmer, self).__init__(bridge=bridge, device_id=device_id, device_type=I2CApplianceType.RGB,
                                           default_state=(0, 0, 0))

    def _encode_state(self, state: Tuple[float, float, float]) -> int:
        try:
            if 0 <= state[0] <= 1 and 0 <= state[1] <= 1 and 0 <= state[2] <= 1:
                return (int(255 * state[0]) << 16) + (int(255 * state[1]) << 8) + (int(state[2] * 255))

            # Not a valid state otherwise
            raise TypeError

        except TypeError:
            raise InvalidStateError(self, state)

    def _decode_state(self, raw_state: int) -> Tuple[float, float, float]:
        return (raw_state >> 16) / 255, ((raw_state >> 8) % 0x100) / 255, (raw_state % 0x100) / 255

    def set_color(self, color: Tuple[float, float, float]) -> None:
        """
        Sets the color of this RGB Dimmer. It is expressed as a RGB color triplet, with values for each color ranging
        from 0 to 1 inclusive.
        :param color: Tuple of red, green and blue colors, each ranging from 0 to 1 inclusive
        """
        self.set_state(color)

    def __str__(self):
        return "RGB Dimmer (%s)" % super().__str__()


class I2CShutter(I2CAppliance):
    """Represents a Shutter appliance."""
    class State(Enum):
        """Enumeration for the Shutter's possible state values."""
        IDLE = 0x00
        UP_ONCE = 0x01
        UP_FULL = 0x02
        DOWN_ONCE = 0x03
        DOWN_FULL = 0x04

    def __init__(self, bridge, device_id: int):
        super(I2CShutter, self).__init__(bridge=bridge, device_id=device_id, device_type=I2CApplianceType.SHUTTER,
                                         default_state=I2CShutter.State.IDLE)

    def _encode_state(self, state: State) -> int:
        try:
            return state.value
        except ValueError:
            raise InvalidStateError(self, state)

    def _decode_state(self, raw_state: int) -> State:
        try:
            return self.State(raw_state)
        except ValueError:
            raise InvalidStateError(self, raw_state)

    def stop(self) -> None:
        """Stops this Shutter from moving."""
        self.set_state(self.State.IDLE)

    def move_up(self) -> None:
        """Moves this Shutter up for one movement cycle."""
        self.set_state(self.State.UP_ONCE)

    def move_up_full(self) -> None:
        """Moves this Shutter up fully."""
        self.set_state(self.State.UP_FULL)

    def move_down(self) -> None:
        """Moves this Shutter down for one movement cycle."""
        self.set_state(self.State.DOWN_ONCE)

    def move_down_full(self) -> None:
        """Moves this Shutter down fully."""
        self.set_state(self.State.DOWN_FULL)

    def __str__(self):
        return f"Shutter ({super().__str__()})"


_DEVICE_CLASSES = {
    I2CApplianceType.BINARY: I2CGenericBinary,
    I2CApplianceType.DIMMER: I2CDimmer,
    I2CApplianceType.RGB: I2CRGBDimmer,
    I2CApplianceType.SHUTTER: I2CShutter,
}