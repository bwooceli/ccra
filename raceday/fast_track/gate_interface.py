#### import csv
from datetime import datetime
import os

import serial
import serial.tools.list_ports

# set date variable with yyyy-MM-dd format
date = datetime.now().strftime("%Y-%m-%d")


class FastTrackGate():
    def __init__(
        self,
        output_file=os.path.join(
            "fast_track_output", f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}.csv"
        ),
        lane_count=3,
        *args,
        **kwargs,
    ):
        self.connected = False

        self.lane_count = lane_count
        possible_lane_names = ["A", "B", "C", "D", "E", "F"]

        # createa a dictionary of lane names and their corresponding lane number
        # for as many lanes as are configured
        self.lane_names = {}
        for i in range(lane_count):
            self.lane_names[possible_lane_names[i]] = str(i + 1)

        self.place_names = {
            "!": {"title": "1st", "position": 1},
            '"': {"title": "2nd", "position": 2},
            "#": {"title": "3rd", "position": 3},
            "D": {"title": "DNF", "position": None},
        }

        self.output_file = output_file

        self.connect_to_gate()

    def connect_to_gate(self):
        print("Attempting gate connection...")

        likely_ports = []
        selection_prompt = "\n"

        # use serial to scan for the gate
        ports = serial.tools.list_ports.comports()
        # Print the device name and port number for each port
        for i, port in enumerate(ports):
            selection_prompt += f"{i+1}. {port.device}: {port.description}\n"
            # if the port.description contains "usb to serial bridge" then it's a likely device
            if "usb to serial" in port.description.lower():
                likely_ports.append(port)

        # if there are no likely ports, or if there more than one,
        # prompt the user to select a port
        if len(likely_ports) != 1:
            print(selection_prompt)
            # Prompt the user to select a port
            selection = input("Select the row for the desired device: ")
            # Get the selected port
            self.com_port = ports[int(selection) - 1].device
            self.com_device = ports[int(selection) - 1].description
        else:
            print(
                f"Found likely port: {likely_ports[0].device} {likely_ports[0].description}"
            )
            self.com_port = likely_ports[0].device
            self.com_device = likely_ports[0].description

        print(f"Attempting port: {self.com_port} {self.com_device}")
        try:
            self.gate = serial.Serial(self.com_port)
            print(f"Connected to {self.com_port} {self.com_device}")
            self.connected = True
        except:
            print(f"Failed to connect to {self.com_port} {self.com_device}")

    def write_to_csv(self, heat_result):
        write_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # write_timestamp with millisecondsB
        heat_result = (
            heat_result.replace("\t", ",").replace("\n", f",{write_timestamp}\n")
            + f",{write_timestamp}\n"
        )
        filename = self.output_file

        # check if filename exists, if not create it
        if not os.path.exists(filename):
            # create directories if needed
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as fd:
                fd.write("Heat,Lane,Car,Time,Position,HeatTimestamp\n")

        with open(filename, "a") as fd:
            fd.write(heat_result)

    def process_result(self, data_raw, heat, lane_cars):
        heat_results = data_raw.split(" ")[0 : len(lane_cars)]
        # print(heat_results)

        # Parse the result and build the output strings
        clipboard_result = ""
        i = 0

        # sample data_raw:
        # '@A=1.758# B=1.392" C=1.086! D=0.000D E=0.000D F=0.000D'
        # print(heat_results)

        for result in heat_results:
            lane = result.split("=")[0][-1:]
            result = result.split("=")[1]
            place_name = self.place_names[result[-1:]]["title"]
            place_position = self.place_names[result[-1:]]["position"]
            print(
                f"Heat {heat}\tLane {self.lane_names[lane]}\tCar {lane_cars[i]}\t{result[0:5]}\t{place_name}"
            )
            clipboard_result += f"{heat}\t{self.lane_names[lane]}\t{lane_cars[i]}\t{result[0:5]}\t{place_position}"
            i += 1
            if i < len(heat_results):
                clipboard_result += "\n"

        self.write_to_csv(clipboard_result)
        return

    def run_race(self, starting_car_number=1, ending_car_number=10):
        print(
            """***************************** IMPORTANT ******************************\n*** Make sure that the lane numbers line up with the gate lanes!!! ***\n"""
        )

        heat = int(input(f"\nEnter Starting Heat Number (Default 1): ") or 1)

        race_running = "y"

        lane_cars = [f"{starting_car_number}", "0", "0"]

        auto_advance_car_lanes = False

        while race_running == "y":
            final_heat = False
            print(f"\nEnter cars for heat {heat}")
            if auto_advance_car_lanes is True:
                lane_cars[2] = lane_cars[1]
                lane_cars[1] = lane_cars[0]
                if int(lane_cars[2]) != ending_car_number: 
                    lane_cars[0] = f"{int(lane_cars[1])+1}"
                else:
                    final_heat = True
            if int(lane_cars[0]) < ending_car_number+1 and final_heat is False: 
                lane_cars[0] = (
                    input(f"   Lane 1 Car #: ({lane_cars[0]}) ") or f"{lane_cars[0]}"
                )
            else:
                lane_cars[0] = "0"
                print(f"   Lane 1 Car #: (0) ")
            
            if int(lane_cars[1] or 0) < ending_car_number+1  and final_heat is False: 
                lane_cars[1] = (
                    input(f"   Lane 2 Car #: ({lane_cars[1]}) ") or f"{lane_cars[1]}"
                )
            else:
                lane_cars[1] = "0"
                print(f"   Lane 2 Car #: (0) ")
                
            if int(lane_cars[2] or 0) < ending_car_number+1: 
                lane_cars[2] = (
                    input(f"   Lane 3 Car #: ({lane_cars[2]}) ") or f"{lane_cars[2]}"
                )

            print(f"\n{lane_cars}")
            go_race = input(
                f"Enter to start heat {heat} or any other key to re-enter cars (q to quit): "
            )

            if go_race != "":
                auto_advance_car_lanes = False
                if go_race == "q":
                    return True
                continue

            print(f"\nHeat {heat} Ready! GO GO GO!", end="\r")
            data_raw = self.gate.readline()
            print("                                        ", end="\r")
            # print(data_raw)
            data_raw = data_raw.decode("utf-8").replace("  ", "D ")
            self.process_result(data_raw, heat, lane_cars)
            auto_advance_car_lanes = True
            
            try:
                if f"{lane_cars[2]}" == f"{ending_car_number}":
                    finish_race = input(f"\nRace Complete!\nPress Enter to quit or O to override: ")
                    if finish_race == "":
                        return True
                heat = int(
                    input(f"\nEnter to begin heat {heat+1} or override: ") or (heat + 1)
                )
            except:
                race_running = "n"

        return True
