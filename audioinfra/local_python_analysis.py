import argparse
import subprocess # nosec
import glob
import sys
import os
from pathlib import Path

PYLINT_FAIL_UNDER=5.0

parser = argparse.ArgumentParser(description='Сканирование уязвимостей Python')
parser.add_argument('-b', '--bandit', action='store_true',
                     help='Сканирование всех Python-файлов через Bandit (уязвимости)')
parser.add_argument('-l', '--pylint', action='store_true',
                     help='Сканирование всех Python-файлов через pylint (статический анализ)')
parser.add_argument('-p', '--pipaudit', action='store_true',
                     help='Сканирование зависимостей pip через pipaudit (уязвимости)')
parser.add_argument('-a', '--all', action='store_true', help='Запуск всего сканирования')

def search_for_python_files():
    """Поиск всех .py файлов в текущем рабочем окружении"""
    parent_path = Path().resolve().parent
    os.chdir(parent_path)
    python_files = glob.glob('**/*.py', recursive=True)

    return python_files

def run_bandit():
    """Анализ через Bandit"""
    python_files = search_for_python_files()

    for file in python_files:
        print(f"Bandit analysis for {file}")
        subprocess.check_call(["bandit", file]) # nosec

def run_pylint():
    """Анализ через Pylint"""
    python_files = search_for_python_files()

    for file in python_files:
        print(f"Pylint analysis for {file}")
        subprocess.check_call(["pylint", f"--fail-under={PYLINT_FAIL_UNDER}", file]) # nosec

def run_pipaudit():
    """Анализ через pipaudit"""
    requirements_files = glob.glob('**/requirements.txt', recursive=True)

    for file in requirements_files:
        print(f"pip-audit analysis for {file}")
        subprocess.check_call(["pip-audit", "-r", file]) # nosec

def run_all():
    """Все типы анализа сразу"""
    run_bandit()
    run_pylint()
    run_pipaudit()

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

if args.bandit:
    run_bandit()

if args.pylint:
    run_pylint()

if args.pipaudit:
    run_pipaudit()

if args.all:
    run_all()
