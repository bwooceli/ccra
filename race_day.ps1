Start-Process -FilePath "powershell" -ArgumentList `
"-noexit .\venvs\prod\Scripts\activate;
python ccra\manage.py run_race"