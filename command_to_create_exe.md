## Run this command where you have your python file

```powershell
python -m PyInstaller --onefile --windowed --icon="battery.ico" --hidden-import "bs4" --hidden-import "lxml" --add-data "battery.ico;." builder.py
```
