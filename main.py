"""
Pings the telegram bot and logs results
All settings are stored in config.ini file

(c) 2021 mtrineyev
"""

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

import logging
logging.basicConfig(
    filename=config['Logging']['FILE_NAME'],
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=int(config['Logging']['LEVEL']))
logging.debug('Script started')

from os import getenv
import requests
from time import sleep
logging.debug('Standart libraries imported')

from telethon import TelegramClient, sync
logging.debug('telethon library imported')


if __name__ == '__main__':
    logging.debug('Main block entered')

    api_id = config['Telegram']['API_ID']
    api_hash = config['Telegram']['API_HASH']
    bot_name = config['Telegram']['BOT_NAME']
    err_report_account = config['Telegram']['ERR_REPORT_ACCOUNT']
    heath_check_url = config['Telegram']['HEALTH_CHECK_URL']
    loop_pause=float(config['Loop']['PAUSE'])

    client = TelegramClient('ping', api_id, api_hash)
    client.start()

    while True:
        if heath_check_url:
            requests.get(f'{heath_check_url}/start', timeout=5)

        client.send_message(bot_name, 'ping')
        sleep(5)
        result = client.get_messages(bot_name, limit=2)
        if result and len(result) == 2 and result[1].text == 'ping':
            logging.warning('PING OK')
            client.delete_messages(bot_name, [result[0].id, result[1].id])
        else:
            logging.error('PING FAILED')
            client.send_message(err_report_account, f'😬 {bot_name} ping failed!')

        if heath_check_url:
            requests.get(heath_check_url)

        if not loop_pause:
            break
        sleep(loop_pause)
