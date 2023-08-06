from unittest import TestCase

from fpga_i2c_bridge.appliance import I2CRGBDimmer, InvalidStateError, I2CDimmer


class TestDimmer(TestCase):
    TESTS_VALID = {
        0: True,
        1: True,
        0.5: True,
        0.9: True,
        1.1: False,
        -1: False,
        "bright": False,
        None: False
    }

    def setUp(self) -> None:
        self.dev = I2CDimmer(None, 0)

    def test_valid_states(self):
        for state, result in self.TESTS_VALID.items():
            try:
                self.dev._encode_state(state)

                if not result:
                    self.fail("State %s should fail but didn't" % str(state))
            except InvalidStateError:
                if result:
                    self.fail("State %s shouldn't fail but did" % str(state))


class TestI2CRGBDimmer(TestCase):
    TESTS = {
        (1.0, 0, 0): 0xFF0000,
        (0, 1.0, 0): 0x00FF00,
        (0, 0, 1.0): 0x0000FF,
        (1.0, 1.0, 1.0): 0xFFFFFF,
        (0.5, 0, 0.5): 0x7F007F
    }

    TESTS_VALID = {
        (0, 0, 0): True,
        (-1, 0, 0): False,
        (256, 0, 0): False,
        ("0", 0, 0): False,
        "red": False,
        (2, 0): False,
        (1, 2, 3, 4): False
    }

    def setUp(self) -> None:
        self.dev = I2CRGBDimmer(None, 0)

    def test_encode_state(self):
        for rgb, hex in self.TESTS.items():
            self.assertEqual(hex, self.dev._encode_state(rgb))

    def test_decode_state(self):
        dev = I2CRGBDimmer(None, 0)

        for rgb, hex in self.TESTS.items():
            r, g, b = rgb
            rr, rg, rb = self.dev._decode_state(hex)

            self.assertAlmostEqual(r, rr, places=1)
            self.assertAlmostEqual(g, rg, places=1)
            self.assertAlmostEqual(b, rb, places=1)

    def test_valid_states(self):
        for state, result in self.TESTS_VALID.items():
            try:
                self.dev._encode_state(state)

                if not result:
                    self.fail("State %s should fail but didn't" % str(state))
            except InvalidStateError:
                if result:
                    self.fail("State %s shouldn't fail but did" % str(state))


