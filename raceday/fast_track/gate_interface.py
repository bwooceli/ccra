import csv
from datetime import datetime

import pyperclip
import serial

from django.conf import settings

def write_to_csv(heat_result):
    write_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    heat_result = heat_result.replace('\t', ',').replace('\n',f',{write_timestamp}\n' )+f',{write_timestamp}\n'
    filename = f"results_{datetime.today().strftime('%Y-%m-%d')}.csv"
    with open(filename,'a') as fd:
        fd.write(heat_result)

def gate_listen():
    heat_results = None

    lane_names = {
        "A": "1",
        "B": "2",
        "C": "3",
    }

    place_names = {
        '!': {"title": "1st", "position": 1},
        '"': {"title": "2nd", "position": 2},
        "#": {"title": "3rd", "position": 3},
        "D": {"title": "DNF", "position": None},
    }

    if hasattr(settings, "DEFAULT_FAST_TRACK_PORT"):
        com_port = settings.DEFAULT_FAST_TRACK_PORT
    else:    
        com_port = input("Enter the port for the FastTrack adapter: ")
        if com_port == "":
            com_port = "COM4"

    if hasattr(settings, "DEFAULT_FAST_TRACK_LANES"):
        lanes = settings.DEFAULT_FAST_TRACK_LANES
    else:
        lanes = 3

    print(f'Attempting port: {com_port}')
    gate = serial.Serial(com_port)
    print("Gate Connected\n")

    heat = int(input(f'\nEnter Starting Heat Number (Default 1): ') or 1) 

    keep_alive = "y"
    lane = ''

    lane_cars = ["1", " ", " "]

    auto_advance_car_lanes = False

    while keep_alive == "y":
        print(f"Enter cars for heat {heat}")
        if auto_advance_car_lanes is True:
            lane_cars[2] = lane_cars[1]
            lane_cars[1] = lane_cars[0]
            lane_cars[0] = f"{int(lane_cars[1])+1}"

        lane_cars[0] = input(f"   Lane 1 Car #: ({lane_cars[0]}) ") or f"{lane_cars[0]}"
        lane_cars[1] = input(f"   Lane 2 Car #: ({lane_cars[1]}) ") or f"{lane_cars[1]}"
        lane_cars[2] = input(f"   Lane 3 Car #: ({lane_cars[2]}) ") or f"{lane_cars[2]}"

        print(f"\n{lane_cars}")
        go_race = input("Enter to start heat or any other key to re-enter cars (q to quit): ")
        if go_race != "":
            auto_advance_car_lanes = False
            if go_race == "q":
                exit()
            continue

        print(f"\nHeat {heat} Ready! GO GO GO!", end='\r')
        data_raw = gate.readline()
        print('                                        ', end='\r')
        # print(data_raw)
        data_raw = data_raw.decode("utf-8").replace("  ", "D ")
        heat_results = data_raw.split(' ')[0:lanes]
        # print(heat_results)
        
        # Parse the result and build the output strings
        clipboard_result = ''
        i = 0
        for result in heat_results:
            lane = result.split('=')[0][-1:]
            result = result.split('=')[1]
            place_name = place_names[result[-1:]]["title"]
            place_position = place_names[result[-1:]]["position"]
            print(f'Heat {heat}\tLane {lane_names[lane]}\tCar {lane_cars[i]}\t{result[0:5]}\t{place_name}')
            clipboard_result += f'{heat}\t{lane_names[lane]}\t{lane_cars[i]}\t{result[0:5]}\t{place_position}'
            i += 1
            if i < len(heat_results):
                clipboard_result += '\n'

        pyperclip.copy(clipboard_result)
        write_to_csv(clipboard_result)
        auto_advance_car_lanes = True
        try:
            heat = int(input(f"\nEnter to begin heat {heat+1} or override: ") or (heat + 1))
        except:
            keep_alive = "n"

    return True
