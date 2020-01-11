FROM python:3.7-stretch

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip \
    && pip install beautifulsoup4 \
    && pip install requests \
    && pip install colorlog \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

CMD [ "python", "./main.py" ]