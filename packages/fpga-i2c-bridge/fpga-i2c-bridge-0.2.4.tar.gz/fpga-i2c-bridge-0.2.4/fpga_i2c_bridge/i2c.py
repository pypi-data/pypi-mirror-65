"""Representations for the I2C bus."""

from abc import ABC
from typing import List, Union

from fpga_i2c_bridge.net.error import I2CNoDataException, I2CRecvCRCFailureException, I2CSendCRCFailureException, I2CException, \
    I2CCommunicationError
from fpga_i2c_bridge.net.packet import I2CGetApplianceStateCommand, I2CGetApplianceTypeCommand, I2CSetApplianceStateCommand, \
    I2CGetFPGAStatusCommand, I2CResetFPGACommand, I2CPollCommand, FPGAStatus, I2CResponse, I2CRepeatLastMessageCommand, \
    I2CGetSensorTypeCommand, I2CCommand, I2CApplianceStateResponse, I2CApplianceTypeResponse, I2CSensorTypeResponse, \
    I2CFPGAStatusResponse, I2CInputEventResponse
from fpga_i2c_bridge.util import Logger


class I2CBus(ABC):
    """
    Abstract class for representing an I2C bbus.
    """
    def __init__(self, max_retries: int = 10, *args, **kwargs):
        self.logger = Logger.get_logger(self)
        self.max_retries = max_retries

    def raw_write(self, request: bytes) -> None:
        """
        Writes the specified byte sequence onto the bus.
        :param request: Bytes to write
        """
        raise NotImplementedError()

    def raw_read(self, request: bytes) -> bytes:
        """
        Writes the specified byte sequence onto the bus, then reads the raw response. This will not perform CRC
        checksum verification on the received data.
        :param request: Bytes to write
        :return: Response bytes
        """
        raise NotImplementedError()

    def cmd_write(self, command: I2CCommand) -> None:
        """
        Writes the specified command onto the bus.
        :param command: Command to write
        """
        self.raw_write(command.ship())

    def cmd_read(self, command: I2CCommand):
        """
        Writes the specified command onto the bus, then reads the response. This will perform CRC checksum verification
        on the received data, and will attempt to request the response again, up until the defined max_retries settings.
        Should the response contain a status code other than OK, it will throw an approprate exception.
        In case the I2C connection fails, this will throw an I2CCommunicationError.
        :param command: Command to write
        :return: Response object
        """
        attempt = 0
        orig_command = command
        while attempt < self.max_retries:
            try:
                attempt += 1
                reply = self.raw_read(command.ship())
                return command.handle_reply(reply)
            except I2CRecvCRCFailureException:
                self.logger.info(f"CRC failure in message from FPGA, requesting re-send "
                                 f"(Attempt {attempt}/{self.max_retries})")
                command = I2CRepeatLastMessageCommand(orig_command)
            except I2CSendCRCFailureException:
                self.logger.info(f"Got CRC error from FPGA, re-sending {attempt}/{self.max_retries})")
                command = orig_command

        raise I2CCommunicationError()

    def get_appliance_state(self, device_id: int) -> I2CApplianceStateResponse:
        """
        Retrieves the state of the appliance with the supplied ID.
        :param device_id: ID of appliance
        :return: Appliance state response
        """
        return self.cmd_read(I2CGetApplianceStateCommand(device_id))

    def get_appliance_type(self, device_id: int) -> I2CApplianceTypeResponse:
        """
        Retrieves the type of the appliance with the supplied ID.
        :param device_id: ID of appliance
        :return: Appliance type response
        """
        return self.cmd_read(I2CGetApplianceTypeCommand(device_id))

    def get_sensor_type(self, sensor_id: int) -> I2CSensorTypeResponse:
        """
        Retrieves the type of the sensor with the supplied ID.
        :param sensor_id: ID of sensor
        :return: Sensor type response
        """
        return self.cmd_read(I2CGetSensorTypeCommand(sensor_id))

    def set_appliance_state(self, device_id: int, new_state: int) -> None:
        """
        Requests to set the state of the appliance with the specified ID to the specified raw state.
        :param device_id: ID of appliance
        :param new_state: New raw state
        """
        self.cmd_read(I2CSetApplianceStateCommand(device_id, new_state))

    def get_fpga_status(self) -> I2CFPGAStatusResponse:
        """
        Retrieves the status of the FPGA bridge.
        :return: FPGA Status response
        """
        return self.cmd_read(I2CGetFPGAStatusCommand())

    def reset_fpga(self) -> None:
        """Resets the FPGA."""
        self.cmd_write(I2CResetFPGACommand())

    def poll(self) -> List[Union[I2CApplianceStateResponse, I2CInputEventResponse]]:
        """
        Polls for new State Update and Input events.
        :return: List of event responses for poll request
        """
        out = []
        while True:
            try:
                out.append(self.cmd_read(I2CPollCommand()))
            except I2CNoDataException:
                break

        return out


class I2CBusReal(I2CBus):
    """Implementation of the I2C bus that uses the hardware's I2C interface through the smbus2 module."""
    def __init__(self, bus, addr, *args, **kwargs):
        super(I2CBusReal, self).__init__(*args, **kwargs)
        self.bus = bus
        self.addr = addr

    def raw_write(self, request: bytes) -> None:
        """
        Writes the specified byte sequence onto the bus.
        Throws an I2CException should the connection fail.
        :param request: Bytes to write
        """
        from smbus2 import SMBusWrapper, i2c_msg
        with SMBusWrapper(self.bus) as bus:
            cmd = i2c_msg.write(self.addr, request)
            try:
                self.logger.debug(">> %s" % " ".join("%02x" % byte for byte in request))
                bus.i2c_rdwr(cmd)
            except IOError:
                raise I2CException("IO error in I2C communication")

    def raw_read(self, request: bytes) -> bytes:
        """
        Writes the specified byte sequence onto the bus, then reads the raw response. This will not perform CRC
        checksum verification on the received data.
        Throws an I2CException should the connection fail.
        :param request: Bytes to write
        :return: Response bytes
        """
        from smbus2 import SMBusWrapper, i2c_msg
        with SMBusWrapper(self.bus) as bus:
            request_cmd = i2c_msg.write(self.addr, request)
            response_cmd = i2c_msg.read(self.addr, 8)

            self.logger.debug(">> %s" % " ".join("%02x" % byte for byte in request))

            try:
                bus.i2c_rdwr(request_cmd)
                bus.i2c_rdwr(response_cmd)

                response = b""
                for byte in response_cmd:
                    response += bytes((byte,))

                self.logger.debug("<< %s" % " ".join("%02x" % byte for byte in response))

                return response

            except IOError:
                raise I2CException("IO error in I2C communication")
