# CoronaStats
A simple discord bot to provide stats & graphs on COVID-19.  
Setup details are listed below, alternatively, you can use [my instance of the bot](https://discordapp.com/oauth2/authorize?client_id=691369979186249799&permissions=604359745&scope=bot).

## Setup
First, ensure you have Python 3.7+. This can be installed [here](https://python.org/download), or on Linux, with:
```bash
$ sudo apt install python3.8
$ sudo apt install python3.8-dev
```
Then, install discord.py. On Windows, as admin:
```batch
> py -m pip install discord.py -U
```
Or Linux:
```bash
$ sudo -H python3.8 -m pip install discord.py -U
```
(replace `python3.8` with your Python installation).
Finally, create a file `config.py` in the directory with the rest of the files, and fill in the following:
```python
API_KEY = 'YOUR_RAPIDAPI_KEY'
TOKEN = 'YOUR_DISCORD_TOKEN'
```
(see [getting an API key](#getting-an-api-key) and [getting a Discord token](#getting-a-discord-token)).
Now to run the file, just do
```batch
> py bot.py
```
on Windows (or just double click bot.py), or
```bash
$ python3.8 bot.py
```
on Linux (again, replace `python3.8` with your Python installation).

## Getting an API Key
To get an API key, you will need to create an account on [RapidAPI](https://rapidapi.com/). It is free.

## Getting a Discord Token
To get a Discord token, sign in to the [Discord Developer Portal](https://discordapp.com/developers), and follow the steps below:  
 1. Make sure you are on the [applications page](https://discordapp.com/developers/applications).  
 2. Click "New Application" in the top right.  
 3. Enter a cool name for your bot! You can change this later.  
 4. On the left menu, click on "Bot", then "Create a Bot".  
 5. Copy your Token. Keep this safe!  
 6. To get your bot's invite link, click "OAuth2" on the sidebar.
 7. Under "Scopes", select "Bot".
 8. In the new box that appears ("Bot Permissions"), select "View Channels", "Send Messages" and "Attach Files".
 9. Scroll up again and copy the link!
