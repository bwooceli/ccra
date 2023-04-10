import random
import time

from django.test import TestCase, override_settings

from unittest.mock import patch

import serial

# from race_track.models import *
from race_track.track_timer_interface import *

DEFAULT_DELAY = 0.2


class MockedSerialInterface(serial.Serial):
    def readline(*args, **kwargs):
        return b'@A=1.758# B=1.392" C=1.086! D=0.000  E=0.000  F=0.000  \r\n'

    @property
    def device(self):
        return f"COM{self.port_number}"

    @property
    def description(self):
        return f"{self.port_description}"

    def __init__(
        self,
        port_number=1,
        port_description="Fake-O USB to Serial Bridge",
        *args,
        **kwargs,
    ):
        self.port_number = port_number
        self.port_description = port_description
        self.connected = False


class MockedInvalidSerialInterface(MockedSerialInterface):
    def __init__(self, *args, **kwargs):
        # throw the serial.serialutil.SerialException
        raise serial.serialutil.SerialException


def mocked_user_input_2(*args, **kwargs):
    mock_input = "2"
    print(f"{args[0]}{mock_input}")
    return mock_input


def mocked_user_input_enter(*args, **kwargs):
    mock_input = ""
    print(f"{args[0]}{mock_input}")
    return mock_input


def mocked_user_input_quit_on_7th_heat(*args, **kwargs):
    mock_input = ""
    if (
        args[0]
        == "Enter to start heat 7 or any other key to re-enter cars (q to quit): "
    ):
        mock_input = "q"
    print(f"{args[0]}{mock_input}")
    return mock_input


def mocked_serial_port_listing_with_no_likely_ports(*args, **kwargs):
    return [
        MockedSerialInterface(
            port_number=4, port_description="Bluetooth Serial Port A "
        ),
        MockedSerialInterface(
            port_number=5, port_description="Bluetooth Serial Port B"
        ),
        MockedSerialInterface(
            port_number=6, port_description="Bluetooth Serial Port C"
        ),
    ]


def mocked_serial_port_listing_with_multiple_likely_ports(*args, **kwargs):
    return [
        MockedSerialInterface(port_number=4, port_description="Bluetooth Serial Port"),
        MockedSerialInterface(
            port_number=5, port_description="FAKE-O USB to Serial Bridge"
        ),
        MockedSerialInterface(
            port_number=6, port_description="CapsuleCorp USB to Serial Bridge"
        ),
    ]


def mocked_serial_port_listing_with_single_likely_port(*args, **kwargs):
    return [
        MockedSerialInterface(port_number=4, port_description="Bluetooth Serial Port"),
        MockedSerialInterface(
            port_number=5, port_description="FAKE-O USB to Serial Bridge"
        ),
        MockedSerialInterface(port_number=6, port_description="Bluetooth Serial Port"),
    ]


def mocked_gate_readline_normal(*args, **kwargs):
    possible_results = [
        b'@A=1.758# B=1.392" C=1.086! D=0.000  E=0.000  F=0.000  \r\n',
        b'A=2.572" B=2.929! @C=2.287#  D=0.000  E=0.000  F=0.000  \r\n',
        b'A=2.572! @B=2.129# C=2.687"  D=0.000  E=0.000  F=0.000  \r\n',
    ]
    time.sleep(DEFAULT_DELAY)
    return random.choice(possible_results)


def mocked_gate_readline_one_dnf(*args, **kwargs):
    time.sleep(DEFAULT_DELAY)
    return b'@A=1.572" B=1.129! C=9.999  D=0.000  E=0.000  F=0.000  \r\n'


def mocked_gate_readline_two_dnf(*args, **kwargs):
    time.sleep(DEFAULT_DELAY)
    return b"@A=2.002! B=9.999  C=9.999  D=0.000  E=0.000  F=0.000  \r\n"


def mocked_gate_readline_all_dnf(*args, **kwargs):
    time.sleep(DEFAULT_DELAY)
    return b"@A=9.999! B=9.999  C=9.999  D=0.000  E=0.000  F=0.000  \r\n"


class GateTestCase(TestCase):
    def setUp(self):
        pass

    def reset_output_file(self, test_method_name):
        output_file = os.path.join(
            "track_output",
            "race_track_output_test",
            f"{test_method_name}.csv",
        )
        # delete the output file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)
        return output_file

    @patch(
        "serial.tools.list_ports.comports",
        mocked_serial_port_listing_with_multiple_likely_ports,
    )
    @patch("builtins.input", mocked_user_input_2)
    @patch("serial.Serial", MockedSerialInterface)
    def test_gate_connection_with_multiple_likely_ports_good_selection(self):
        output_file = self.reset_output_file(self._testMethodName)
        track = FastTrackGate(output_file=output_file)
        self.assertEqual(True, track.connected)

    @patch(
        "serial.tools.list_ports.comports",
        mocked_serial_port_listing_with_single_likely_port,
    )
    @patch("serial.Serial", MockedSerialInterface)
    def test_gate_connection_with_single_likely_ports(self):
        output_file = self.reset_output_file(self._testMethodName)
        track = FastTrackGate(output_file=output_file)
        self.assertEqual(True, track.connected)

    @patch("serial.Serial", MockedInvalidSerialInterface)
    @patch(
        "serial.tools.list_ports.comports",
        mocked_serial_port_listing_with_single_likely_port,
    )
    def test_gate_connection_with_invalid_serial_interface(self):
        output_file = self.reset_output_file(self._testMethodName)
        track = FastTrackGate(output_file=output_file)
        self.assertEqual(False, track.connected)

    @patch("serial.Serial", MockedSerialInterface)
    @patch("serial.Serial.readline", mocked_gate_readline_normal)
    @patch(
        "serial.tools.list_ports.comports",
        mocked_serial_port_listing_with_single_likely_port,
    )
    @patch("builtins.input", mocked_user_input_enter)
    def test_heats(self):
        output_file = self.reset_output_file(self._testMethodName)
        track = FastTrackGate(output_file=output_file)

        ending_car_number = 10

        self.assertEqual(True, track.connected)
        race_complete = track.run_race(
            starting_car_number=1, ending_car_number=ending_car_number
        )
        self.assertEqual(True, race_complete)

        # assert that the last line of the output file
        # has the correct car number in it
        with open(output_file, "r") as f:
            last_line = f.readlines()[-1]
            self.assertEqual(f"{ending_car_number}", last_line.split(",")[2])

    # @patch("serial.Serial", MockedSerialInterface)
    # @patch("serial.Serial.readline", mocked_gate_readline_normal)
    # @patch(
    #     "serial.tools.list_ports.comports",
    #     mocked_serial_port_listing_with_single_likely_port,
    # )
    # @patch("builtins.input", mocked_user_input_quit_on_7th_heat)
    # def test_heats_early_ending(self):
    #     output_file = self.reset_output_file(self._testMethodName)
    #     track = FastTrackGate(
    #         output_file=output_file
    #     )
    #     self.assertEqual(True, track.connected)
    #     race_complete = track.run_race(starting_car_number=1, ending_car_number=10)
    #     self.assertEqual(True, race_complete)

    #     # assert that the first character of the last line of
    #     # the output file is a '6'
    #     with open(output_file, "r") as f:
    #         last_line = f.readlines()[-1]
    #         self.assertEqual('6', last_line[0])

    # @patch("serial.Serial", MockedSerialInterface)
    # @patch("serial.Serial.readline", mocked_gate_readline_normal)
    # @patch("serial.tools.list_ports.comports", mocked_serial_port_listing_with_single_likely_port)
    # def test_heats_with_user_input(self):
    #     self.reset_output_file(self._testMethodName)
    #     track = FastTrackGate()
    #     self.assertEqual(True, track.connected)
    #     race_complete = track.run_race(starting_car_number=1, ending_car_number=4)
    #     self.assertEqual(True, race_complete)

    # def test_gate_connection_with_real_device(self):
    #     self.reset_output_file(self._testMethodName)
    #     print("\ntest_gate_connection_with_real_device")
    #     track = FastTrackGate()
    #     self.assertEqual(True, track.connected)
