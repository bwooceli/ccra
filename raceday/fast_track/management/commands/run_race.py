from lib2to3.pytree import Base
from django.core.management.base import BaseCommand, CommandError

from fast_track import gate_interface

class Command(BaseCommand):
    help = "Connect to the track gate and run the race"

    def handle(self, *args, **kwargs):
        track = gate_interface.FastTrackGate()
        track.run_race()
