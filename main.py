"""
Pings the Telegram bot and logs results

(c) 2021 Maksym Trineyev
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

import argparse
import requests
from time import sleep
logging.debug('Standart libraries imported')

from telethon import TelegramClient
logging.debug('Telethon library imported')

parser = argparse.ArgumentParser(
    prog=f'python3 main.py',
    usage='%(prog)s [option]',
    description='The tool of pinging the Telegram bot'
)
parser.add_argument('-b', '--bot', type=str,
    help='name of the bot to ping (overwrites the variable from config.ini)')

bot_name = parser.parse_args().bot or config['Telegram']['BOT_NAME']
try:
    er_report = config['Telegram'].getint('ERR_REPORT_ACCOUNT')
except ValueError:
    er_report = config['Telegram']['ERR_REPORT_ACCOUNT']
heath_check_url = config['Misc']['HEALTH_CHECK_URL']
ping_word = config['Telegram']['PING_WORD']

client = TelegramClient(
    config['Telegram']['SESSION'],
    config['Telegram']['API_ID'],
    config['Telegram']['API_HASH'])

async def ping() -> None:
    """
    Sends ping to the bot and analyzes the result
    """
    logging.debug('Ping function entered')
    await client.start()
    if heath_check_url:
        requests.get(f'{heath_check_url}/start', timeout=5)
    try:
        await client.send_message(bot_name, ping_word)
        sleep(config['Misc'].getfloat('PAUSE'))
        result = await client.get_messages(bot_name, limit=2)
    except:
        result = None
    if result and len(result) == 2 and result[1].text == ping_word:
        logging.warning(f'Ping {bot_name} OK')
        await client.delete_messages(bot_name, [result[0].id, result[1].id])
    else:
        logging.error(f'Ping {bot_name} FAILED')
        try:
            await client.send_message(er_report, f'😬 {bot_name} ping FAILED!')
        except:
            logging.critical(
                f'Ping {bot_name} error message sending to {er_report} FAILED')
    if heath_check_url:
        requests.get(heath_check_url)
    return


if __name__ == '__main__':
    logging.debug('Main section entered')
    with client:
        client.loop.run_until_complete(ping())
