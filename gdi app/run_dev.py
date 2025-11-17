#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dev runner para reiniciar la app al guardar archivos .py
Requiere: watchdog
"""
import os
import sys
import time
import subprocess
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except Exception as e:
    print("ERROR: watchdog no instalado. Instala con: pip install watchdog")
    sys.exit(1)

APP_ENTRY = "main.py"  # punto de entrada de la app

class RestartOnChange(FileSystemEventHandler):
    def __init__(self, start_func):
        self.start_func = start_func
        self.proc = None
        self.debounce_ts = 0

    def on_any_event(self, event):
        # Solo .py
        if not event.src_path.endswith(".py"):
            return
        # Debounce 0.2s
        now = time.time()
        if now - self.debounce_ts < 0.2:
            return
        self.debounce_ts = now
        print(f"[watch] Cambio detectado en: {event.src_path}")
        self.restart()

    def restart(self):
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=3)
            except Exception:
                self.proc.kill()
        self.proc = self.start_func()

def start_app():
    print("[dev] Iniciando aplicación...")
    return subprocess.Popen([sys.executable, APP_ENTRY])

def main():
    root = Path(__file__).parent.resolve()
    if not (root / APP_ENTRY).exists():
        print(f"ERROR: No se encuentra {APP_ENTRY} en {root}")
        sys.exit(1)

    runner = RestartOnChange(start_app)
    runner.proc = start_app()

    observer = Observer()
    observer.schedule(runner, path=str(root), recursive=True)
    observer.start()

    print("[watch] Observando cambios en *.py (Ctrl+C para salir)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[watch] Saliendo...")
    finally:
        observer.stop()
        observer.join()
        if runner.proc and runner.proc.poll() is None:
            runner.proc.terminate()

if __name__ == "__main__":
    main()
