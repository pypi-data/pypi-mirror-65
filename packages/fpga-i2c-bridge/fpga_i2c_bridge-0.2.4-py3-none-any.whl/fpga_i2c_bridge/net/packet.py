"""Gateway to FPGA smart bridge protocol, containing command and response representations."""
from __future__ import annotations
from collections import namedtuple
from typing import Union

from fpga_i2c_bridge.net.error import I2CUnknownOpcodeException, I2CNoSuchDeviceException, I2CException, I2CNoDataException, \
    I2CRecvCRCFailureException, I2CSendCRCFailureException
from fpga_i2c_bridge.util.crc import crc16

OP_APPLIANCE_GET_STATE = 0x00
OP_APPLIANCE_GET_TYPE = 0x01
OP_SENSOR_GET_TYPE = 0x02

OP_APPLIANCE_SET_STATE = 0x10

OP_FPGA_GET_STATUS = 0x20
OP_FPGA_RESET = 0x2F

OP_POLL = 0x30

OP_REPEAT_LAST_MESSAGE = 0x40

POLL_TYPE_INPUT = 0x00
POLL_TYPE_UPDATE = 0x01

STATUS_OK = 0xF0
STATUS_ERROR = 0xF1
STATUS_NO_DATA = 0xF2

ERR_UNKNOWN_CMD = 0x10
ERR_NO_SUCH_DEVICE = 0x20
ERR_CRC_FAILURE = 0x30
ERR_UNKNOWN_FAILURE = 0xFF


_EXCEPTIONS = {
    ERR_UNKNOWN_CMD: lambda x: I2CUnknownOpcodeException(*x),
    ERR_NO_SUCH_DEVICE: lambda x: I2CNoSuchDeviceException(*x),
    ERR_CRC_FAILURE: lambda x: I2CSendCRCFailureException(),
    ERR_UNKNOWN_FAILURE: lambda x: I2CException("FPGA reported unknown failure")
}

FPGAStatus = namedtuple('FPGAStatus', 'version num_outputs num_inputs')


class I2CCommand:
    """Base class for I2C commands."""
    def __init__(self, opcode: int):
        self.opcode = opcode

    def parameters(self) -> tuple:
        """
        Returns the raw parameter data as an iterable of ints. When translating a command object into bytes, these
        values will be used as the command parameters, following the command's opcode.
        """
        return ()

    def handle_reply(self, reply: bytes) -> I2CResponse:
        """
        This method handles a response from the FPGA.
        Because the response does not indicate its type, each command dictates the kind of response it expects.
        Should the response contain a status code other than OK, this will throw the appropriate exception.
        :param reply: FPGA response data
        :return: Response object
        """

        # Verify CRC checksum first
        if crc16(reply) > 0:
            raise I2CRecvCRCFailureException()

        # Handle error responses and raise appropriate exceptions
        if reply[0] == STATUS_ERROR:
            try:
                raise _EXCEPTIONS[reply[1]](reply[2:])
            except KeyError:
                raise I2CException("Unknown error of type %02x reported" % reply[1])

        # Handle no data responses
        if reply[0] == STATUS_NO_DATA:
            raise I2CNoDataException()

        # Return the constructed response object
        return self.construct_reply(reply[1:])

    def construct_reply(self, reply: bytes) -> I2CResponse:
        """
        Constructs a response object from the FPGA response bytes and returns it.
        By default, this returns an empty response.
        :param reply: FPGA response data
        :return: Response object
        """
        return I2CResponse()

    def ship(self) -> bytes:
        """
        Translates itself to its byte representation.
        :return: Command as bytes
        """
        msg = bytes((self.opcode,) + self.parameters())
        crc = crc16(msg)
        return msg + int.to_bytes(crc, 2, 'big')


class I2CSetApplianceStateCommand(I2CCommand):
    """
    Represents a Set Appliance State command.
    This command does not expect a response.
    """
    def __init__(self, device_id: int, new_state: int):
        super(I2CSetApplianceStateCommand, self).__init__(OP_APPLIANCE_SET_STATE)
        self.device_id = device_id
        self.new_state = new_state

    def parameters(self) -> tuple:
        """
        Defines the Set Appliance State command's parameters.
        :return: Tuple of appliance ID and new 3-byte raw state value, MSB first.
        """
        return self.device_id, (self.new_state >> 16) & 0xFF, (self.new_state >> 8) & 0xFF, self.new_state & 0xFF


class I2CGetApplianceStateCommand(I2CCommand):
    """
    Represents a Get Appliance State command.
    This command expects a response containing the device ID and state.
    """
    def __init__(self, device_id: int):
        super(I2CGetApplianceStateCommand, self).__init__(OP_APPLIANCE_GET_STATE)
        self.device_id = device_id

    def parameters(self) -> tuple:
        """
        Defines the Get Appliance State command's parameters.
        :return: Tuple of device ID
        """
        return self.device_id,

    def construct_reply(self, reply: bytes) -> I2CApplianceStateResponse:
        """
        Constructs the Get Appliance State response.
        :param reply: FPGA response data
        :return: Appliance state response, containing device ID and three-byte state, MSB first
        """
        return I2CApplianceStateResponse(device_id=reply[0],
                                         device_state=(reply[1] << 16) + (reply[2] << 8) + reply[3])


class I2CGetApplianceTypeCommand(I2CCommand):
    """
    Represents a Get Appliance Type command.
    This command expects a response containing the device ID and its type.
    """
    def __init__(self, device_id: int):
        super(I2CGetApplianceTypeCommand, self).__init__(OP_APPLIANCE_GET_TYPE)
        self.device_id = device_id

    def parameters(self) -> tuple:
        """
        Defines the Get Appliance Type command's parameters.
        :return: Tuple of appliance ID
        """
        return self.device_id,

    def construct_reply(self, reply: bytes) -> I2CApplianceTypeResponse:
        """
        Constructs the Get Appliance Type response.
        :param reply: FPGA response data
        :return: Appliance type response, containing device ID and type
        """
        return I2CApplianceTypeResponse(device_id=reply[0], device_type=reply[1])


class I2CGetSensorTypeCommand(I2CCommand):
    """
    Represents a Get Sensor Type command.
    This command expects a response containing the sensor device ID and its type.
    """
    def __init__(self, sensor_id: int):
        super(I2CGetSensorTypeCommand, self).__init__(OP_SENSOR_GET_TYPE)
        self.sensor_id = sensor_id

    def parameters(self) -> tuple:
        """
        Defines the Get Sensor Type command's parameters.
        :return: Tuple of sensor device ID
        """
        return self.sensor_id,

    def construct_reply(self, reply: bytes) -> I2CSensorTypeResponse:
        """
        Constructs the Get Sensor Type response.
        :param reply: FPGA response data
        :return: Sensor Type reply, containing sensor device ID and type
        """
        return I2CSensorTypeResponse(sensor_id=reply[0], sensor_type=reply[1])


class I2CGetFPGAStatusCommand(I2CCommand):
    """
    Represents a Get FPGA Status Command.
    Expects a response containing two-byte FPGA version, MSB first, as well as highest IDs of appliances and sensors,
    respectively.
    """
    def __init__(self):
        super(I2CGetFPGAStatusCommand, self).__init__(OP_FPGA_GET_STATUS)

    def construct_reply(self, reply: bytes) -> I2CFPGAStatusResponse:
        """
        Constructs the Get FPGA Status Command response.
        :param reply: FPGA response data
        :return: Get FPGA Status response, containing two-byte FPGA version, MSB first, as well as highest IDs of
        appliances and sensors.
        """
        return I2CFPGAStatusResponse(version=(reply[0] << 8) + reply[1],
                                     num_appliances=reply[2], num_sensors=reply[3])


class I2CResetFPGACommand(I2CCommand):
    """
    Represents a Reset FPGA command.
    This command does not expect a response.
    """
    def __init__(self):
        super(I2CResetFPGACommand, self).__init__(OP_FPGA_RESET)


class I2CPollCommand(I2CCommand):
    """
    Represents a Poll command.
    This command expects a response containing either a State Update or Input event.
    """
    def __init__(self):
        super(I2CPollCommand, self).__init__(OP_POLL)

    def construct_reply(self, reply: bytes) -> Union[I2CApplianceStateResponse, I2CInputEventResponse]:
        """
        Constructs the Poll response.
        Should the response contain an unknown event type, a I2CException will be thrown.
        :param reply: FPGA response data
        :return: Either one of Appliance State or Input Event response
        """
        if reply[0] == POLL_TYPE_UPDATE:
            return I2CApplianceStateResponse(device_id=reply[1],
                                             device_state=(reply[2] << 16) + (reply[3] << 8) + reply[4])

        elif reply[0] == POLL_TYPE_INPUT:
            return I2CInputEventResponse(sensor_id=reply[1],
                                         sensor_data=(reply[2] << 16) + (reply[3] << 8) + reply[4])

        else:
            raise I2CException("Unknown event type %02x received" % reply[0])


class I2CRepeatLastMessageCommand(I2CCommand):
    """
    Represents a Repeat Last Message command.
    The expected response depends on the command that was sent prior.
    """
    def __init__(self, last_command: I2CCommand):
        super(I2CRepeatLastMessageCommand, self).__init__(OP_REPEAT_LAST_MESSAGE, )
        self.last_command = last_command

    def construct_reply(self, reply: bytes) -> I2CResponse:
        """
        Constructs a Repeat Last Message response.
        :param reply: FPGA response data
        :return: Response to the command that was sent prior to this one.
        """
        return self.last_command.construct_reply(reply)


class I2CResponse:
    """Base class for FPGA responses."""
    pass


class I2CFPGAStatusResponse(I2CResponse):
    """
    Represents a FPGA Status response.
    """
    def __init__(self, version, num_appliances: int, num_sensors: int):
        super(I2CFPGAStatusResponse, self).__init__()

        """FPGA version"""
        self.version = version

        """Highest ID of appliances"""
        self.num_appliances = num_appliances

        """Highest ID of sensors"""
        self.num_sensors = num_sensors


class I2CApplianceStateResponse(I2CResponse):
    """
    Represents an Appliance State response.
    """
    def __init__(self, device_id: int, device_state: int):
        super(I2CApplianceStateResponse, self).__init__()
        """ID of appliance"""
        self.device_id = device_id
        """Appliance's new raw state"""
        self.device_state = device_state


class I2CApplianceTypeResponse(I2CResponse):
    """
    Represents an Appliance Type response.
    """
    def __init__(self, device_id: int, device_type: int):
        super(I2CApplianceTypeResponse, self).__init__()
        """ID of appliance"""
        self.device_id = device_id
        """Appliance's type"""
        self.device_type = device_type


class I2CSensorTypeResponse(I2CResponse):
    """
    Represents a Sensor Type response.
    """
    def __init__(self, sensor_id: int, sensor_type: int):
        super(I2CSensorTypeResponse, self).__init__()
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type


class I2CInputEventResponse(I2CResponse):
    """
    Represents an Input Event response.
    """
    def __init__(self, sensor_id: int, sensor_data: int):
        super(I2CInputEventResponse, self).__init__()
        """ID of sensor"""
        self.sensor_id = sensor_id

        """Data that was sent"""
        self.sensor_data = sensor_data
