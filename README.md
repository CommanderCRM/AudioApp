# Серверная часть приложения для оценки качества речи

## Требования

- Docker >19.03.0
- Docker Compose >1.27

## Установка

```git clone https://github.com/CommanderCRM/AudioApp.git``` (HTTPS) либо ```git clone git@github.com:CommanderCRM/AudioApp.git``` (SSH).
Данные действия (Clone) можно также производить через интерфейс среды разработки.
Полученный сервер готов к использованию.

## Запуск

- Перейти в директорию ```audioinfra```
- ```docker compose up```

### Локальный запуск

- Получить .tar-архивы с образами Docker
- Перенести их в директорию ```audioinfra```
- Запустить скрипт ```local_dockers.py``` в данной директории с параметром ```-i``` либо ```--install```
- После установки образов ввести ```docker compose up```
- Для распознавания речи получить .zip архив модели Vosk (например vosk-model-ru-0.22) [отсюда](https://alphacephei.com/vosk/models), распаковать в директорию ```audioserver/logic/audiorecognition```

- Для доступа к основному контейнеру Docker локально можно использовать ```docker run --rm -it --entrypoint /bin/bash -v *репозиторий*:/app audiodocker```

### Локальное сканирование уязвимостей

- Для сканирования уязвимостей Docker-образов при наличии их в директории ```audioinfra``` можно использовать параметр ```local_dockers.py -t```
- Для сканирования уязвимостей кода Python и зависимостей pip можно вызвать скрипт ```local_python_analysis.py -a``` в директории ```audioinfra```. Должны быть установлены модули ```bandit```, ```pip-audit```, ```pylint```.

### Локальное модульное тестирование

- Установить системный пакет ```sqlite3```. Перейти в ```audioserver/tests```.
- Создать БД на основе ```sqlite3.sql```: ```sqlite3 sqlite3.db < sqlite3.sql```.
- Установить переменную среды ```TESTING``` (```export TESTING=1```).
- Запустить в интерактивном режиме docker в ```audioinfra```: ```docker compose run --rm --entrypoint=/bin/bash audio```
- Далее выполнить ```pytest -rA .``` в ```audioserver/tests```.
- После прохождения тестов можно удалить ```sqlite3.db```

## Доступ к локальному серверу

- ```localhost:48080``` в адресной строке браузера/Postman/прочего, также через серверы и клиенты. Пример: ```localhost:48080/docs```

## Остановка

- ```Ctrl+C```
- ```docker compose down```

## Полезное

- Для получения информации о новых изменениях репозитория: ```git fetch --all``` либо Fetch через среду разработки.
- При новых изменениях репозитория они применяются через ```git pull *удаленный репозиторий/ветка*``` либо Pull через среду разработки.
- Для удаления БД нужно удалить директорию ```data``` внутри ```audioinfra/sqldocker```.
