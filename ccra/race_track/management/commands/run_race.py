from lib2to3.pytree import Base
from django.core.management.base import BaseCommand, CommandError

from race_track import track_timer_interface

class Command(BaseCommand):
    help = "Connect to the track gate and run the race"

    def add_arguments(self, parser):
        parser.add_argument("starting_car_number", type=int)
        parser.add_argument("ending_car_number", type=int)

    def handle(self, *args, **kwargs):
        # set the starting and ending car numbers from the command line
        starting_car_number = kwargs["starting_car_number"]
        ending_car_number = kwargs["ending_car_number"]

        track = track_timer_interface.TrackTimer()
        track.run_race(starting_car_number, ending_car_number)
