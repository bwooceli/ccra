from django.test import TestCase, override_settings

from unittest.mock import patch

import serial

# from fast_track.models import *
from fast_track.gate_interface import *

class MockedSerialInterface(serial.Serial):
    def readline(*args, **kwargs):
        return b'@A=1.758# B=1.392" C=1.086! D=0.000  E=0.000  F=0.000  \r\n'

    def __init__(self, *args, **kwargs):
        pass

def mocked_gate_readline_normal(*args, **kwargs):
    return b'@A=1.758# B=1.392" C=1.086! D=0.000  E=0.000  F=0.000  \r\n'

def mocked_gate_readline_one_dnf(*args, **kwargs):
    return b'@A=1.572" B=1.129! C=9.999  D=0.000  E=0.000  F=0.000  \r\n'

def mocked_gate_readline_two_dnf(*args, **kwargs):
    return b'@A=2.002! B=9.999  C=9.999  D=0.000  E=0.000  F=0.000  \r\n'

def mocked_gate_readline_all_dnf(*args, **kwargs):
    return b'@A=9.999! B=9.999  C=9.999  D=0.000  E=0.000  F=0.000  \r\n'


class GateTestCase(TestCase):
    def setUp(self):
        pass

    @patch("serial.Serial.readline", mocked_gate_readline_normal)
    def test_gate_normal_heat(self):
        self.assertEqual(True, gate_listen())

    # @patch("serial.Serial.readline", mocked_gate_readline_one_dnf)
    # def test_gate_one_dnf_heat(self):
    #     self.assertEqual(True, gate_listen())

    # @patch("serial.Serial.readline", mocked_gate_readline_two_dnf)
    # def test_gate_two_dnf_heat(self):
    #     self.assertEqual(True, gate_listen())

    # @patch("serial.Serial.readline", mocked_gate_readline_all_dnf)
    # def test_gate_all_dnf_heat(self):
    #     self.assertEqual(True, gate_listen())

    # @override_settings()
    # @patch("serial.Serial", MockedSerialInterface)
    # @patch("serial.Serial.readline", mocked_gate_readline_normal)
    # def test_gate_no_port_setting_found(self):
    #     del settings.DEFAULT_FAST_TRACK_PORT
    #     self.assertEqual(True, gate_listen())

    # @override_settings()
    # @patch("serial.Serial", MockedSerialInterface)
    # @patch("serial.Serial.readline", mocked_gate_readline_normal)
    # def test_gate_no_port_setting_found_no_user_input(self):
    #     del settings.DEFAULT_FAST_TRACK_PORT
    #     self.assertEqual(True, gate_listen())


