py.exe -m venv .\venvs\prod
.\venvs\prod\Scripts\activate
py.exe -m pip install --upgrade pip
py.exe -m pip install -r requirements.txt
cd .\ccra
py.exe .\manage.py migrate
py.exe .\manage.py collectstatic --noinput
py.exe .\manage.py createsuperuser
coverage run --source='.' manage.py test
