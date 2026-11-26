import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def _ensure_chromium():
    # Streamlit Cloud has no Playwright browser by default; install once per container.
    marker = os.path.expanduser("~/.cache/ms-playwright/.installed_by_app")
    if not os.path.exists(marker):
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=False)
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        open(marker, "w").close()


_ensure_chromium()

import runpy

runpy.run_path(os.path.join(SRC, "demo_ui.py"), run_name="__main__")
