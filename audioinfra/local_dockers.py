import argparse
import subprocess
import os

def save_images():
    """Получение списка образов Docker в системе и сохранение их в .tar архивы"""
    command = ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}']
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    images = result.stdout.split('\n')

    for image in images:
        if image:
            file_name = image.replace('/', '_').rstrip(':-')
            command = ['docker', 'save', '-o', f'{file_name}.tar', image]
            subprocess.run(command, check=True)

def install_images():
    """Установка образов Docker из архивов .tar"""
    files = os.listdir('.')

    tar_files = [file for file in files if file.endswith('.tar')]

    for file in tar_files:
        command = ['docker', 'load', '-i', file]
        subprocess.run(command, check=True)

HELP_MESSAGE='Данный скрипт позволяет сохранить Docker-образы в архивы .tar и установить их из .tar'
parser = argparse.ArgumentParser(description=f'{HELP_MESSAGE}')
parser.add_argument('-s', '--save', action='store_true', help='Сохранение образов Docker в .tar')
parser.add_argument('-i', '--install', action='store_true', help='Установка образов Docker из .tar')
args = parser.parse_args()

if args.save:
    save_images()
elif args.install:
    install_images()
else:
    parser.print_help()
