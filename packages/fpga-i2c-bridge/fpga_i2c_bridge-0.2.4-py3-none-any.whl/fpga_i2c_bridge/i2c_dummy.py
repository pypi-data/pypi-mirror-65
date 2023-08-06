"""A dummy implementation of the I2C bus that simulates a real bridge."""

import threading
from collections import deque
from random import random
from time import sleep
from typing import List, Optional

from fpga_i2c_bridge.appliance import I2CShutter
from fpga_i2c_bridge.i2c import I2CBus
from fpga_i2c_bridge.net.packet import OP_APPLIANCE_GET_STATE, STATUS_OK, OP_APPLIANCE_GET_TYPE, OP_APPLIANCE_SET_STATE, \
    OP_FPGA_GET_STATUS, OP_FPGA_RESET, STATUS_ERROR, ERR_NO_SUCH_DEVICE, ERR_UNKNOWN_CMD, OP_POLL, STATUS_NO_DATA, \
    POLL_TYPE_UPDATE, OP_REPEAT_LAST_MESSAGE, ERR_CRC_FAILURE, OP_SENSOR_GET_TYPE
from fpga_i2c_bridge.util import Logger
from fpga_i2c_bridge.util.crc import crc16


def split_state(state: int):
    return state >> 24, (state >> 16) % 0x100, state % 0x100


class I2CDummyDevice:
    def __init__(self, i2c, device_type, device_id):
        self.i2c = i2c
        self.type = device_type
        self.device_id = device_id
        self.state = 0

    def set_state(self, state: bytes):
        self.state = (state[0] << 16) + (state[1] << 8) + state[2]

    def update(self):
        pass


class I2CDummySwitch(I2CDummyDevice):
    def __init__(self, *args, **kwargs):
        super(I2CDummySwitch, self).__init__(device_type=1, *args, **kwargs)


class I2CDummyDimmer(I2CDummyDevice):
    def __init__(self, *args, **kwargs):
        super(I2CDummyDimmer, self).__init__(device_type=2, *args, **kwargs)


class I2CDummyRGB(I2CDummyDevice):
    def __init__(self, *args, **kwargs):
        super(I2CDummyRGB, self).__init__(device_type=3, *args, **kwargs)


class I2CDummyShutter(I2CDummyDevice):
    def __init__(self, *args, **kwargs):
        super(I2CDummyShutter, self).__init__(device_type=4, *args, **kwargs)
        self.timer = 0

    def set_state(self, state):
        super().set_state(state)
        encoded = I2CShutter.State(self.state)
        if encoded == I2CShutter.State.UP_ONCE or encoded == I2CShutter.State.DOWN_ONCE:
            self.timer = 10
        elif encoded == I2CShutter.State.UP_FULL or encoded == I2CShutter.State.DOWN_FULL:
            self.timer = 50
        else:
            self.timer = 0

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.i2c.queue_update(self.device_id, I2CShutter.State.IDLE.value)


_DUMMY_DEVICE_TYPES = {
    1: I2CDummySwitch,
    2: I2CDummyDimmer,
    3: I2CDummyRGB,
    4: I2CDummyShutter
}


class I2CDummy(I2CBus):
    def __init__(self, appliance_types: List[int], sensor_types: Optional[List[int]] = None, error_ratio: float = 0.0, *args, **kwargs):
        super(I2CDummy, self).__init__(*args, **kwargs)
        self.error_ratio = error_ratio
        self.last_message = b""

        self._appliances = {}
        for dev_id, dev_type in enumerate(appliance_types):
            self._appliances[dev_id] = _DUMMY_DEVICE_TYPES[dev_type](i2c=self, device_id=dev_id)

        self._sensors = sensor_types or []

        self._updates = deque()

        self._update_thread = threading.Thread(target=self._device_update_thread, daemon=True)
        self._update_thread.start()

    def _dummy_response(self, *r_bytes) -> bytes:
        out = b""
        for i in range(6):
            out += b"\0" if i >= len(r_bytes) else bytes((r_bytes[i],))

        out += int.to_bytes(crc16(out), 2, 'big')

        self.last_message = out

        if self.error_ratio > 0:
            out = self._glitch(out)

        return out

    def _glitch(self, data: bytes) -> bytes:
        if self.error_ratio == 0:
            return data

        out = b""
        for i in range(len(data)):
            byte = data[i]
            for n in range(8):
                if random() < self.error_ratio:
                    byte = byte ^ (1 << n)
            out += bytes((byte,))

        return out

    def _reset(self):
        for dev in self._appliances.values():
            dev.set_state(b"\0\0\0")

    def _has_device(self, device_id):
        return device_id in self._appliances.keys()

    def _dummy_read(self, request: bytes) -> bytes:
        if crc16(request) > 0:
            self.logger.debug("Req: %s CRC: %d" % (bytes.hex(request), crc16(request)))
            self.logger.info("CRC failure in message from bridge, requesting re-send")
            return self._dummy_response(STATUS_ERROR, ERR_CRC_FAILURE)

        opcode = request[0]

        if opcode == OP_APPLIANCE_GET_STATE:
            device_id = request[1]
            if self._has_device(device_id):
                return self._dummy_response(STATUS_OK, device_id, *split_state(self._appliances[device_id].state))
            else:
                return self._dummy_response(STATUS_ERROR, ERR_NO_SUCH_DEVICE, device_id)

        elif opcode == OP_APPLIANCE_GET_TYPE:
            device_id = request[1]
            if self._has_device(device_id):
                return self._dummy_response(STATUS_OK, device_id, self._appliances[device_id].type)
            else:
                return self._dummy_response(STATUS_OK, device_id, 0)

        elif opcode == OP_SENSOR_GET_TYPE:
            input_id = request[1]
            try:
                input_type = self._sensors[input_id]
                return self._dummy_response(STATUS_OK, input_id, input_type)
            except KeyError:
                return self._dummy_response(STATUS_ERROR, ERR_NO_SUCH_DEVICE, input_id)

        elif opcode == OP_APPLIANCE_SET_STATE:
            device_id = request[1]
            self._appliances[device_id].set_state(request[2:5])
            if self._has_device(device_id):
                return self._dummy_response(STATUS_OK)
            else:
                return self._dummy_response(STATUS_ERROR, ERR_NO_SUCH_DEVICE, device_id)

        elif opcode == OP_FPGA_GET_STATUS:
            return self._dummy_response(STATUS_OK, 0xde, 0xad, len(self._appliances), len(self._sensors))

        elif opcode == OP_POLL:
            if len(self._updates) > 0:
                return self._updates.popleft()

            return self._dummy_response(STATUS_NO_DATA)

        elif opcode == OP_REPEAT_LAST_MESSAGE:
            return self._glitch(self.last_message)

        elif opcode == OP_FPGA_RESET:
            self._reset()
            return self._dummy_response(STATUS_OK)

        else:
            return self._dummy_response(STATUS_ERROR, ERR_UNKNOWN_CMD, opcode)

    def queue_update(self, device_id: int, state: int):
        self.logger.debug("Received device state update: Device %d, State %06x" % (device_id, state))
        self._updates.append(self._dummy_response(STATUS_OK, POLL_TYPE_UPDATE, device_id, *split_state(state)))

    def _device_update_thread(self):
        self.logger.info("Starting dummy device update thread")

        try:
            while True:
                for device in self._appliances.values():
                    device.update()

                sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Closing dummy device update thread")

    def raw_write(self, request: bytes) -> None:
        self._dummy_read(request)
        self.logger.debug(">> %s" % " ".join("%02x" % byte for byte in request))

    def raw_read(self, request: bytes) -> bytes:
        self.logger.debug(">> %s" % " ".join("%02x" % byte for byte in request))

        response = self._dummy_read(self._glitch(request))

        self.logger.debug("<< %s" % " ".join("%02x" % byte for byte in response))

        return response
