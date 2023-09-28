import argparse
import subprocess # nosec
import os

CURRENT_DIR = os.getcwd()

def save_images():
    """Получение списка образов Docker в системе и сохранение их в .tar архивы"""
    command = ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}']
    result = subprocess.run(command, capture_output=True, text=True, check=True) # nosec
    images = result.stdout.split('\n')

    for image in images:
        if image:
            file_name = image.replace('/', '_').rstrip(':-')
            command = ['docker', 'save', '-o', f'{file_name}.tar', image]
            subprocess.run(command, check=True) # nosec

def install_images():
    """Установка образов Docker из архивов .tar"""
    files = os.listdir('.')

    tar_files = [file for file in files if file.endswith('.tar')]

    for file in tar_files:
        command = ['docker', 'load', '-i', file]
        subprocess.run(command, check=True) # nosec

def scan_images():
    """Сканирование Docker-образов на наличие уязвимостей"""
    command = ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}']
    result = subprocess.run(command, capture_output=True, text=True, check=True) # nosec
    images = result.stdout.split('\n')

    for image in images:
        if image:
            file_name = image.replace('/', '_').rstrip(':-')
            scan_command = ['docker', 'run', '--rm', '-v',
                            '/var/run/docker.sock:/var/run/docker.sock',
                            '-v', f'{CURRENT_DIR}:/workdir', 'aquasec/trivy:0.45.1', 'image',
                            '--input', f'./workdir/{file_name}.tar']
            subprocess.run(scan_command, check=True) # nosec


HELP_MESSAGE_1='Данный скрипт позволяет сохранить Docker-образы в .tar-архивы, установить их.'
HELP_MESSAGE_2=' Дополнительно можно просканировать образы на наличие уязвимостей'
HELP_MESSAGE=HELP_MESSAGE_1+HELP_MESSAGE_2

parser = argparse.ArgumentParser(description=f'{HELP_MESSAGE}')
parser.add_argument('-s', '--save', action='store_true', help='Сохранение образов Docker в .tar')
parser.add_argument('-i', '--install', action='store_true', help='Установка образов Docker из .tar')
parser.add_argument('-t', '--trivy-scan', action='store_true', help='Сканирование образов Docker')
args = parser.parse_args()

if args.save:
    save_images()
elif args.install:
    install_images()
elif args.trivy_scan:
    scan_images()
else:
    parser.print_help()
