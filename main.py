import requests
import csv
import configparser
import random
import re
import logger
import mail
from bs4 import BeautifulSoup
from threading import Thread

errors = []


class MyThread(Thread):
    """
    Основной класс потока
    """

    def __init__(self, row, logger):
        Thread.__init__(self)
        self.row = row
        self.logger = logger

    def run(self) -> None:
        domain = row.get('domain')
        logger = self.logger

        logger.info('Calling thread: {}'.format(domain))

        try:
            check(self.row)
        except ConnectionError as err:
            errors.append('{domain} - Connection error: {err}'.format(domain=domain, err=err))
            logger.error('{domain} - Connection error: {err}'.format(domain=domain, err=err))
        except Exception as err:
            errors.append('{domain} - Undefined error: {err}'.format(domain=domain, err=err))
            logger.error('{domain} - Undefined error: {err}'.format(domain=domain, err=err))


def check(row):
    """
    Проверка шагов оплаты
    :param row:
    :return:
    """
    with requests.session() as s:
        url = '{protocol}://{domain}'.format(
            protocol=config.get('default', 'protocol'),
            domain=row.get('domain')
        )

        r = s.get(url)

        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.select('a')
        filter_links = []

        for link in links:
            if re.search(r'\/catalog\/Bestsellers\/', str(link.get('href'))):
                filter_links.append(link.get('href'))

        link = random.choice(filter_links)

        r = s.get(link)

        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all('a')
        filter_links = []

        for link in links:
            if re.search(r'\?buy=\d+', str(link.get('href'))):
                filter_links.append(link.get('href'))

        link = random.choice(filter_links)

        r = s.get(link)

        soup = BeautifulSoup(r.content, 'html.parser')
        form = soup.find('form', attrs={'id': 'checkoutForm'})
        link = form.get('action')
        textarea = soup.find('textarea', attrs={'id': 'resultArrC'})

        r = s.post(link, data={
            'resultArrC': textarea.text
        })

        soup = BeautifulSoup(r.content, 'html.parser')
        form = soup.find('form', attrs={'id': 'formOk'})
        link = form.get('action')
        textarea = soup.find('textarea', attrs={'name': 'resultArrC'})

        r = s.post(link, data={
            'resultArrC': textarea.text
        })

        if r.status_code == 200:
            logger.info('{status} - {url}'.format(status=r.status_code, url=url))
        else:
            logger.warning('{status} - {url}'.format(status=r.status_code, url=url))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    logger = logger.init_logger(__name__, testing_mode=False)
    threads = []

    with open('domain.csv') as file:
        reader = csv.DictReader(file)

        for row in reader:
            thread = MyThread(row, logger)
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    if errors:
        mail.send_email('Domain check errors', '\n'.join(errors), config.get('mail', 'destination'))
