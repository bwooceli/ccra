Get-ChildItem -Recurse -Directory -Filter "migrations" | ForEach-Object {
    $directoryPath = $_.FullName
    Get-ChildItem -Path $directoryPath -Exclude "__init__.py" -Recurse | Remove-Item -Recurse -Force
}
rm .\db.sqlite3
py.exe ./manage.py makemigrations
py.exe ./manage.py migrate
