@echo off
REM Ejecuta el dev runner con auto-reload (requiere watchdog)
python -m pip install watchdog --quiet
python run_dev.py
