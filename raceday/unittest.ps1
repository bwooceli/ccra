# check to see if virtual environment is active
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not active. Activate the virtual environment and try again."
    exit
}

coverage run --source='.' manage.py test
coverage html

# open the coverage report
start htmlcov\index.html