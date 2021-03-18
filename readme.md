# Telegram Bot ping

## Description
Python script Telegram-client for testing if selected Telegram bot is alive

## Setup and deployment
- `git clone` this repository
- `cd pingbot`
- set variables in `config.ini`. How to get API ID: `https://telethon.readthedocs.io/en/latest/basic/signing-in.html`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python main.py`
- enter telephon number for your API ID for first auth
- and set cron rules for the script running
