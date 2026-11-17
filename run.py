"""
Medical AI Chatbot — Entry Point (Port 8501)
Run: python run.py
"""
import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
    ]
    sys.exit(stcli.main())
