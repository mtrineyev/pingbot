import logging
logging.basicConfig(
    filename='pingbot.log',
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

from os import getenv
import requests
from time import sleep

from dotenv import load_dotenv
from telethon import TelegramClient, sync


if __name__ == '__main__':
    load_dotenv()
    api_id = getenv('API_ID')
    api_hash = getenv('API_HASH')
    bot_name = getenv('BOT_NAME')
    err_report_account = getenv('ERR_REPORT_ACCOUNT')
    heath_check_url = getenv('HEALTH_CHECK_URL')

    requests.get(f'{heath_check_url}/start', timeout=5)

    client = TelegramClient('ping_session', api_id, api_hash)
    client.start()
    client.send_message(bot_name, 'ping')
    sleep(5)
    result = client.get_messages(bot_name, limit=2)
    if result and len(result) == 2 and result[1].text == 'ping':
        logging.info('PING OK')
        client.delete_messages(bot_name, [result[0], result[1]])
    else:
        logging.error('PING FAILED')
        client.send_message(err_report_account, f'😬 {bot_name} ping failed!')

    requests.get(heath_check_url)
