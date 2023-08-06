"""Contains specialized exception classes for I2C communication."""

class I2CException(BaseException):
    """Base I2C exception. This gets thrown when a generic I2C communication error occurs."""
    def __init__(self, message):
        super(I2CException, self).__init__(message)


class I2CUnknownOpcodeException(I2CException):
    """Exception that gets thrown when the FPGA reported an unknown opcode."""
    def __init__(self, opcode, *_):
        super(I2CUnknownOpcodeException, self).__init__("FPGA received unknown opcode: %02x" % opcode)
        self.opcode = opcode


class I2CNoSuchDeviceException(I2CException):
    """Exception that gets thrown when the FPGA reported that an unknown device has been addressed."""
    def __init__(self, device_id, *_):
        super(I2CNoSuchDeviceException, self).__init__("FPGA reported unknown device ID %02x" % device_id)
        self.device_id = device_id


class I2CNoDataException(I2CException):
    """Exception that gets thrown when no data is available for  a polling request."""
    def __init__(self):
        super(I2CNoDataException, self).__init__("FPGA reported no data")


class I2CSendCRCFailureException(I2CException):
    """Exception that gets thrown when the API encountered erroneous CRC data from the FPGA."""
    def __init__(self):
        super(I2CSendCRCFailureException, self).__init__("CRC failure during sending")


class I2CRecvCRCFailureException(I2CException):
    """Exception that gets thrown when the FPGA reported a CRC error in a transmission from the API."""
    def __init__(self):
        super(I2CRecvCRCFailureException, self).__init__("CRC failure during receiving")


class I2CCommunicationError(I2CException):
    """Exception that gets thrown when too many CRC errors happened in a row, aborting the communication."""
    def __init__(self):
        super(I2CCommunicationError, self).__init__("I2C communication failure: Too many CRC errors")
