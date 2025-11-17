@echo off
setlocal

REM === 1) Verificar Python en PATH ===
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se encontro 'python' en el PATH. Instala Python 3.11+ desde python.org.
  pause
  exit /b 1
)

REM === 2) Crear entorno virtual si no existe ===
if not exist ".venv" (
  echo [INFO] Creando entorno virtual .venv ...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
  )
)

REM === 3) Asegurar pip dentro del venv y actualizarlo ===
call ".venv\Scripts\python" -m ensurepip --upgrade
call ".venv\Scripts\python" -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERROR] Fallo al actualizar pip en el venv.
  pause
  exit /b 1
)

REM === 4) Instalar dependencias necesarias ===
echo [INFO] Instalando dependencias base...
call ".venv\Scripts\python" -m pip install ^
  mysql-connector-python ^
  pyinstaller ^
  python-dotenv
if errorlevel 1 (
  echo [ERROR] Fallo al instalar dependencias.
  pause
  exit /b 1
)


REM === 5) Iniciar la aplicacion ===
echo [INFO] Iniciando la aplicacion...
call ".venv\Scripts\python" main.py

endlocal
