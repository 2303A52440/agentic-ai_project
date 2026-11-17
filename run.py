"""
MediAssist AI — Port 3000 Entry Point
Run: python run.py
"""
import sys
import subprocess
from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port=3000",
        "--server.address=0.0.0.0",
    ]
    sys.exit(stcli.main())
