import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# Streamlit Cloud has no Playwright browser by default. Install it in the
# background so the UI renders right away; it is ready after about a minute.
_MARKER = os.path.expanduser("~/.cache/ms-playwright/.installed_by_app")


def _install_chromium():
    cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
    subprocess.run(cmd, check=False)
    os.makedirs(os.path.dirname(_MARKER), exist_ok=True)
    open(_MARKER, "w").close()


if not os.path.exists(_MARKER) and not os.environ.get("_PW_INSTALL_STARTED"):
    os.environ["_PW_INSTALL_STARTED"] = "1"
    import threading

    threading.Thread(target=_install_chromium, daemon=True).start()

import runpy

runpy.run_path(os.path.join(SRC, "demo_ui.py"), run_name="__main__")
