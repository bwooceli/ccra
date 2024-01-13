# Overview

Currently, this software is primarily an interface for the Fast Track Model K3 V1.0 Timer Gate.  It will facilitate capturing data from the timer and storing it in a CSV.  

Work is underway to make it a Django application that can use a local SQLite database or connect to a database server.  SQLite will be used by default.

## Hardware

This has been tested on Windows 11 AMD with a USB->Serial adapter connected to a Fast Track Model K3 V1.0 Timer Gate

## Python version
This has been tested with Python 3.11 and 3.12

## Bootstrapping
run the bootstrap script with

    .\bootstrap.ps1

This will create a virtual environment and install the required packages and run a series of tests to ensure the environment is working properly. 

## Race Day script
Run the race with 

    .\race_day.ps1

 * ALL raw data from the track device will be saved to the `device_logs` directory.

 * Formatted race results will be saved to the `race_output` directory.

## Tests
Tests can be run with:

    coverage run --source='.' manage.py test
