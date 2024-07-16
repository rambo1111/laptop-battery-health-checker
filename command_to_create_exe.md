```powershell
python -m PyInstaller --onefile --windowed --icon="battery.ico" --hidden-import "bs4" --hidden-import "lxml" --add-data "battery.ico;." main.py
```