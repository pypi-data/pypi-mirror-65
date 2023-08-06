from unittest import TestCase

from fpga_i2c_bridge import I2CBridge, I2CApplianceType, I2CSensorType


class TestI2C(TestCase):
    APPLIANCES = [4, 3, 2, 1]
    SENSORS = [2, 3, 1, 4, 5]
    VERSION = 0xdead

    def setUp(self) -> None:
        self.i2c = I2CBridge(i2c_dummy=True, i2c_dummy_appliances=self.APPLIANCES, i2c_dummy_sensors=self.SENSORS)

    def test_get_devices(self):
        self.assertEqual(len(self.i2c.appliances), len(self.APPLIANCES))
        self.assertEqual(len(self.i2c.sensors), len(self.SENSORS))

        for i, dev_type in enumerate(self.APPLIANCES):
            self.assertEqual(self.i2c.appliances[i].device_type, I2CApplianceType(dev_type))

        for i, dev_type in enumerate(self.SENSORS):
            self.assertEqual(self.i2c.sensors[i].sensor_type, I2CSensorType(dev_type))

    def test_version(self):
        # Dummy I2C version
        self.assertEqual(self.i2c.version, self.VERSION)