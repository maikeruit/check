## Инструкция по установке

В системе должен быть установлен `python3` и для работы с докер пакет `docker` так же должен быть установлен.

В `python` скрипте используются пакеты `beautifulsoup4`, `requests`, `colorlog`.

Домены указываются в файле `domain.csv`, протокол подключения к доменам настраивается в`config.ini`.

#### Установка с использованием Virtual env

Введите в терминале:

```bash
python3 -m venv venv
source ./venv/bin/active
pip install beautifulsoup4
pip install requests
pip install colorlog
python main.py
```

#### Установка пакетов в систему

Введите в терминале: 

```bash
pip3 install beautifulsoup4
pip3 install requests
pip3 install colorlog
python3 main.py
```

#### Запуск через Docker

Введите в терминале:

```bash
docker build -t script .
docker run -it --rm -v $(pwd):/usr/src/app script
```