# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.makedirs("logs", exist_ok=True)

API_PORT = int(os.environ.get("API_PORT", "8011"))
UI_PORT = int(os.environ.get("UI_PORT", "8511"))
py = sys.executable

backend = subprocess.Popen(
    [py, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(API_PORT)],
    cwd=str(ROOT),
    stdout=open("logs/backend.log", "w", encoding="utf-8"),
    stderr=subprocess.STDOUT,
)
time.sleep(1.2)
if backend.poll() is not None:
    print("Backend failed to start. See logs/backend.log")
    sys.exit(1)
print("Backend ready  http://127.0.0.1:%s" % API_PORT)

env = os.environ.copy()
env["API_BASE"] = "http://127.0.0.1:%s" % API_PORT
frontend = subprocess.Popen(
    [py, "-m", "streamlit", "run", "frontend/app.py",
     "--server.port", str(UI_PORT), "--server.headless", "true"],
    cwd=str(ROOT),
    env=env,
    stdout=open("logs/frontend.log", "w", encoding="utf-8"),
    stderr=subprocess.STDOUT,
)
time.sleep(2.0)
url = "http://localhost:%s" % UI_PORT
print("Frontend      %s" % url)
try:
    webbrowser.open(url)
except Exception:
    pass
print("Stop: Ctrl+C")
try:
    frontend.wait()
except KeyboardInterrupt:
    pass
finally:
    for p in (frontend, backend):
        if p.poll() is None:
            p.terminate()
