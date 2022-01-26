from django.test import TestCase

from fast_track.models import *
from fast_track.gate_interface import *

class GateTestCase(TestCase):
    def setUp(self):
        pass

    def test_gate_connected(self):
        self.assertEqual(True, gate_listen())
