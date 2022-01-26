# Assumptions

Assuming the Fast Track (tm) Pinewood Derby Gate and an IO Gear serial -> USB adapter, you will need to have [this driver](https://www.iogear.com/support/dm/driver/GUC232A)

Change the settings for these values based on your local system in raceday.settings
  - DEFAULT_FAST_TRACK_PORT = "COM4"
  - DEFAULT_FAST_TRACK_LANES = 3

Tests can be run with:

    coverage run --source='.' manage.py test
