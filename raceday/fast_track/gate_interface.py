from sys import exec_prefix
import serial

from django.conf import settings

def gate_listen():
    heat_results = None
    com_port = ""
    try:
        com_port = settings.DEFAULT_FAST_TRACK_PORT
    except:
        com_port = input("Enter the port for the FastTrack adapter: ")
        if com_port == "":
            com_port = "COM4"

    try:
        lanes = settings.DEFAULT_FAST_TRACK_LANES
    except:
        lanes = 3

    print(f'Attempting port: {com_port}')

    gate = serial.Serial(com_port)

    keep_alive = "y"
    lane = ''
    while keep_alive == "y":
        data_raw = gate.readline()
        data_raw = data_raw.decode("utf-8")
        print(data_raw)
        heat_results = data_raw.split(' ')[0:lanes]
        for result in heat_results:
            lane = result.split('=')[0]
            result = result.split('=')[1]
            print(f'lane: {lane}\t{result[0:5]}')
        keep_alive = input("Continue (y/n): ")

    return True
