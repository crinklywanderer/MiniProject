#miniproject/run.py


import subprocess
import threading
import webbrowser
import time
import os


def run_backend():
    # Run the backend on port 5000 (Flask default)
    os.environ['FLASK_APP'] = 'backend.app'
    subprocess.run(["python",
                    "-m",
                    "flask",
                    "run",
                    "--host=127.0.0.1",
                    "--port=5000"])

def run_frontend():
    os.chdir("frontend")
    subprocess.run(["python",
                    "-m",
                    "http.server",
                    "8000"])


# Start the backend in a separate thread
backend_thread = threading.Thread(target=run_backend)
backend_thread.daemon = True
backend_thread.start()


# Give the backend a few seconds to boot up
time.sleep(3)


# Start the frontend in a separate thread
frontend_thread = threading.Thread(target=run_frontend)
frontend_thread.daemon = True
frontend_thread.start()


# Open browser to frontend
time.sleep(1)
webbrowser.open("http://localhost:8000")


# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
