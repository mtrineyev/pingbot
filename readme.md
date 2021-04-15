# Telegram Bot ping


## Description
Python script using Telegram-client API for testing if the selected Telegram bot is alive


## Setup and deployment
- `git clone https://github.com/mtrineyev/pingbot.git`
- `cd pingbot`
- `cp config.ini.example config.ini`
- `nano config.ini` and set the variables as described in the comments
- `sudo apt-get install python3-dev`
- `sudo apt-get install python3-venv`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python connect.py` and enter your phone and the code you will recieve
- `nano pingbot.sh` and copy the code below
```
#!/bin/bash
cd ~/pingbot
source venv/bin/activate
python main.py
deactivate
```
- `chmod +x pingbot.sh`


## To run the ping
- `~/pingbot/pingbot.sh`
- you may setup `crontab -e` to run pingbot by schedule


## The tools
- `connect.py` - creates new connection to Telegram client or shows information about active connection, if any


## Licence
The script is free software written by Maksym Trineyev (mtrineyev@gmail.com).

It comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.
