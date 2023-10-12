#!/bin/bash

# Скачивание дистрибутива
wget http://www.pygost.cypherpunks.ru/pygost-5.12.tar.zst
wget http://www.pygost.cypherpunks.ru/pygost-5.12.tar.zst.{asc,sig}

# Проверка подписи
zstd -d < pygost-5.12.tar.zst | tar xf -

# Установка
cd pygost-5.12 || exit
python setup.py install

# Очистка
rm -rf ./pygost-5.12*