# Testing

## Unit Tests

The unittest.ps1 script wraps

    coverage run --source='.' manage.py test
    coverage html

There is an optional argument to the powershell script to launch the html report in your default browser.

    .\unittest.ps1 view-coverage


# Tailwinds
Run in dev mode, will reload changes automatically

    py .\manage.py tailwind start

Run this before pushing to production, will minify the css.  No further steps needed.

    py .\manage.py tailwind build