# Craft Car Racing Alliance

This software is used to manage the Craft Car Racing Alliance. It is a Django application that uses a PostgreSQL database. 

## Hardware

This has been tested on Windows 11 AMD with a USB->Serial adapter connected to a Fast Track Model K3 V1.0 Timer Gate

## Race Day script
Run the race with 

    .\race_day.ps1


## Tests
Tests can be run with:

    coverage run --source='.' manage.py test
