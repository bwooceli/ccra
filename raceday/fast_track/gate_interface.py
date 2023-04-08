#### import csv
from datetime import datetime
import os

import pyperclip
import serial
import serial.tools.list_ports

from django.conf import settings


class FastTrack():
    def __init__(self):
        defaults = settings.FAST_TRACK_DEFAULTS
        self.connected = False
        
        possible_lane_names = ["A", "B", "C", "D", "E", "F"]

        self.lane_names = defaults.get(
            "lane_names",
            {
                "A": "1",
                "B": "2",
                "C": "3",
            },
        )

        self.place_names = defaults.get(
            "place_names",
            {
                "!": {"title": "1st", "position": 1},
                '"': {"title": "2nd", "position": 2},
                "#": {"title": "3rd", "position": 3},
                "D": {"title": "DNF", "position": None},
            },
        )

        self.lanes = defaults.get("lanes", 3)
        self.com_port = defaults.get("port", None)
        if self.com_port == None:
            # use serial to scan for the gate
            ports = serial.tools.list_ports.comports()
            # Print the device name and port number for each port
            for i, port in enumerate(ports):
                print(f"{i+1}. {port.device}: {port.description}")
            # Prompt the user to select a port
            selection = input("Select the row for the USB to Serial Bridge device: ")

            # Get the selected port
            self.com_port = ports[int(selection)-1].device

        print(f"Attempting port: {self.com_port}")
        try:
            self.gate = serial.Serial(self.com_port)
            print(f"Connected to {self.com_port}")
            self.connected = True
        except:
            print(f"Failed to connect to {self.com_port}")

    def write_to_csv(self, heat_result):
        write_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        heat_result = (
            heat_result.replace("\t", ",").replace("\n", f",{write_timestamp}\n")
            + f",{write_timestamp}\n"
        )
        filename = f"results_2023-01-28.csv"

        # check if filename exists, if not create it
        if not os.path.exists(filename):
            with open(filename, "w") as fd:
                fd.write("Heat,Lane,Car,Time,Position,HeatTimestamp\n")

        # if os.stat(filename).st_size == 0:
        #     with open(filename, 'a') as fd:
        #         fd.write('Heat,Lane,Car,Time,Position,HeatTimestamp\n')
        with open(filename, "a") as fd:
            fd.write(heat_result)

    def process_result(self, data_raw, heat, lane_cars):
        heat_results = data_raw.split(" ")[0 : len(lane_cars)]
        # print(heat_results)

        # Parse the result and build the output strings
        clipboard_result = ""
        i = 0
        for result in heat_results:
            lane = result.split("=")[0][-1:]
            result = result.split("=")[1]
            place_name = place_names[result[-1:]]["title"]
            place_position = place_names[result[-1:]]["position"]
            print(
                f"Heat {heat}\tLane {lane_names[lane]}\tCar {lane_cars[i]}\t{result[0:5]}\t{place_name}"
            )
            clipboard_result += f"{heat}\t{lane_names[lane]}\t{lane_cars[i]}\t{result[0:5]}\t{place_position}"
            i += 1
            if i < len(heat_results):
                clipboard_result += "\n"

        pyperclip.copy(clipboard_result)
        self.write_to_csv(clipboard_result)
        return

    def gate_listen(self):
        ##### heat_results = None

        print(
            """***************************** IMPORTANT ******************************\n*** Make sure that the lane numbers line up with the gate lanes!!! ***"""
        )

        print("Gate Connected\n")

        heat = int(input(f"\nEnter Starting Heat Number (Default 1): ") or 1)

        keep_alive = "y"
        ##### lane = ''

        lane_cars = ["1", " ", " "]

        auto_advance_car_lanes = False

        while keep_alive == "y":
            print(f"Enter cars for heat {heat}")
            if auto_advance_car_lanes is True:
                lane_cars[2] = lane_cars[1]
                lane_cars[1] = lane_cars[0]
                lane_cars[0] = f"{int(lane_cars[1])+1}"

            lane_cars[0] = (
                input(f"   Lane 1 Car #: ({lane_cars[0]}) ") or f"{lane_cars[0]}"
            )
            lane_cars[1] = (
                input(f"   Lane 2 Car #: ({lane_cars[1]}) ") or f"{lane_cars[1]}"
            )
            lane_cars[2] = (
                input(f"   Lane 3 Car #: ({lane_cars[2]}) ") or f"{lane_cars[2]}"
            )

            print(f"\n{lane_cars}")
            go_race = input(
                "Enter to start heat or any other key to re-enter cars (q to quit): "
            )
            if go_race != "":
                auto_advance_car_lanes = False
                if go_race == "q":
                    exit()
                continue

            print(f"\nHeat {heat} Ready! GO GO GO!", end="\r")
            with open("Now Racing.csv", "w") as fd:
                output = "Heat,Car\n"
                for car in lane_cars:
                    output += f"{heat},{car}\n"
                fd.write(output)
            data_raw = gate.readline()
            print("                                        ", end="\r")
            # print(data_raw)
            data_raw = data_raw.decode("utf-8").replace("  ", "D ")
            self.process_result(data_raw, heat, lane_cars)
            auto_advance_car_lanes = True
            try:
                heat = int(
                    input(f"\nEnter to begin heat {heat+1} or override: ") or (heat + 1)
                )
            except:
                keep_alive = "n"

        return True
