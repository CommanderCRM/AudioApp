import argparse
import subprocess # nosec
import glob
import sys
import re
import os
from pathlib import Path

PYLINT_FAIL_UNDER=8.0

parser = argparse.ArgumentParser(description='Сканирование уязвимостей Python')
parser.add_argument('-b', '--bandit', action='store_true',
                     help='Сканирование всех Python-файлов через Bandit (уязвимости)')
parser.add_argument('-l', '--pylint', action='store_true',
                     help='Сканирование всех Python-файлов через pylint (статический анализ)')
parser.add_argument('-p', '--pipaudit', action='store_true',
                     help='Сканирование зависимостей pip через pipaudit (уязвимости)')
parser.add_argument('-a', '--all', action='store_true', help='Запуск всего сканирования')

def search_for_python_files():
    """Поиск всех .py файлов в текущем рабочем окружении, кроме модели vosk"""
    parent_path = Path().resolve().parent
    os.chdir(parent_path)
    all_python_files = glob.glob('**/*.py', recursive=True)
    python_files = [f for f in all_python_files if "vosk-model-" not in f]

    return python_files

def run_bandit():
    """Анализ через Bandit"""
    python_files = search_for_python_files()

    for file in python_files:
        print(f"Анализ Bandit файла {file}")
        subprocess.check_call(["bandit", file]) # nosec

def run_pylint():
    """Анализ через Pylint"""
    python_files = search_for_python_files()
    scores = []
    total_files = 0

    for file in python_files:
        print(f"Анализ Pylint файла {file}")
        result = subprocess.run(["pylint", f"--fail-under={PYLINT_FAIL_UNDER}", file], capture_output=True, text=True, check=True) # nosec
        print(result.stdout)
        match = re.search(r'Your code has been rated at (\d+\.\d+)', result.stdout)
        if match is not None:
            score = float(match.group(1))
            scores.append(score)
            total_files += 1

    if total_files > 0:
        combined_score = sum(scores) / total_files
        min_score = min(scores)
        print(f"Минимальный рейтинг Pylint: {min_score:.2f}")
        print(f"Комбинированный рейтинг Pylint: {combined_score:.2f}")
    else:
        print("Не найдено файлов Python")

def run_pipaudit():
    """Анализ через pipaudit"""
    requirements_files = glob.glob('**/requirements.txt', recursive=True)

    for file in requirements_files:
        print(f"Анализ зависимостей pip-audit файла {file}")
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
