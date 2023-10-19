import os
import subprocess
import threading
import pathlib

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'

FILE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = FILE_DIR.parent
SERVER_DIR = PROJECT_DIR / "audioserver"

def setup_and_run(server_name):
    """Установка зависимостей и запуск серверов"""
    venv_dir = f"/opt/venv_{server_name}"
    subprocess.check_call(["python3", "-m", "venv", venv_dir]) # nosec
    subprocess.check_call([f"{venv_dir}/bin/pip", "install", # nosec
                           "-r", f"{FILE_DIR}/pydocker/requirements.txt"]) # nosec
    os.chdir(SERVER_DIR)
    subprocess.check_call([f"{venv_dir}/bin/python", "-m", "uvicorn", f"{server_name}:app", # nosec
                            "--host", "0.0.0.0", # nosec
                            "--port", "48080" if server_name == 'doctor_server' else "50080"]) # nosec

#Каждый сервер запускается в своем потоке
threads = []
for server in ["doctor_server", "patient_server"]:
    thread = threading.Thread(target=setup_and_run, args=(server,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
