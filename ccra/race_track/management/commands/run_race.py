from lib2to3.pytree import Base

import datetime
import os

from django.core.management.base import BaseCommand, CommandError

from race_track import track_timer_interface


class Command(BaseCommand):
    help = "Connect to the track gate and run the race"

    def add_arguments(self, parser):
        # the following arguments should be optional:
        parser.add_argument("race_data_output_file", type=str, nargs="?", default="")
        parser.add_argument("starting_car_number", type=int, nargs="?", default=0)
        parser.add_argument("ending_car_number", type=int, nargs="?", default=0)

    def handle(self, *args, **kwargs):
        # set the starting and ending car numbers from the command line
        race_data_output_file_name = kwargs["race_data_output_file"]
        starting_car_number = kwargs["starting_car_number"]
        ending_car_number = kwargs["ending_car_number"]

        # if the raw data output file is not specified, prompt the user for it
        if race_data_output_file_name == "":
            unit_name = input(
                "        Enter unit name (eg 'Pack 3456', default is '3456): "
            )
            if unit_name == "":
                unit_name = "3456"

            race_type = input(
                "Enter race type (eg 'Cubs' or 'Outlaw', default is 'Cubs'): "
            )
            if race_type == "":
                race_type = "Cubs"

            current_date_string = datetime.datetime.now().strftime("%Y-%m-%d")

            race_data_output_file_name = (
                f"{current_date_string}_{unit_name}_{race_type}.csv"
            )

        if starting_car_number > ending_car_number:
            raise CommandError(
                "Starting car number must be less than ending car number"
            )

        if starting_car_number == 0:
            starting_car_number = input("Enter the starting car number: ")
            try:
                starting_car_number = int(starting_car_number)
            except ValueError:
                raise CommandError("Starting car number must be an integer")

        if ending_car_number == 0:
            ending_car_number = input("Enter the ending car number: ")
            try:
                ending_car_number = int(ending_car_number)
            except ValueError:
                raise CommandError("Ending car number must be an integer")

        track = track_timer_interface.TrackTimer()
        track.output_file = os.path.join("race_output", race_data_output_file_name)
        track.run_race(starting_car_number, ending_car_number)
