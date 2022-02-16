# Telethon shilling bot
## Overview
Bot connect to a user account and send messages to list of groups in loop mode.
User have full control of the script via telegram bot 

### Files
* *main.py* - The bot itself. This file has to be executed with Python to run.
* *funcs.py* - funcs of the bot.
* *config.py* - configuration of the bot
* *keyboards.py* - keyboards for the bot.
* *bot_states.py* - memory states for the bot
* *groups.json* - saved groups to send message to
* *db.json* - users settings
* *requirements.txt* - this file holds all dependencies (Python modules) that are required to run the bot. Once all dependencies are installed, the file is not needed anymore.
* *ReadMe.md* - the readme file you are reading right now. Includes instructions on how to run and use the bot. The file is not needed.

### Available commands  
* `/start` -  to cancel the current action
* `/canel` -  to cancel the current action


* `Set message` - Set new message to the bot
* `Set delay` - Set delay for sending messages
* `Manage groups` - Return list of your groups
##Configuration
Before starting up the bot you have to take care of some settings. You need to edit *config.py* file:

_bot_token_ need to be created using [BotFather](https://t.me/botfather)
## Installing
In order to run the bot you need to execute the script `main.py`. I recommend you to run the script on VPS server,
but you can also run it on Heroku or any other virtual machine. You can also run the script locally on your computer for testing purposes.

#### Python version
You have to use Python 3.7 or above to execute the script

#### Installing needed modules from `requirements.txt` 
Install a set of module-versions that is known to work together for sure (highly recommended):
`pip3 install -r requirements.txt`

or

you can install the modules separately

`pip3 install aiogram`

`pip3 install telethon`

## Starting
To start the script, execute
`python3 main.py`
