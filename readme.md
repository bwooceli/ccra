# Craft Car Racing Alliance

This software is used to manage the Craft Car Racing Alliance. It is a Django application that can use a local SQLite database or connect to a database server.  SQLite is used by default.

## Hardware

This has been tested on Windows 11 AMD with a USB->Serial adapter connected to a Fast Track Model K3 V1.0 Timer Gate

## Race Day script
Run the race with 

    .\race_day.ps1

 * ALL raw data from the track device will be saved to the `device_logs` directory.

 * Formatted race results will be saved to the `race_output` directory.

## Tests
Tests can be run with:

    coverage run --source='.' manage.py test
