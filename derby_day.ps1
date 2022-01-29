Start-Process -FilePath "powershell" -ArgumentList `
"-noexit .\venvs\derby_prod\Scripts\activate;
python raceday\manage.py run_race"