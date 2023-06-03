# Features

Once installed, the program will launch a Discord Bot at computer startup and search a few webtoon scanning websites for chapters every hour.

When the bot is online, use the `!toread` commande to see what chapters you have to read.  

Ping the bot with `!ping` and stop it with `!close`

(WIP) Select which webtoon you read by double-clicking on GUI.ps1

# Installation
## 1. Python librairies
First of all, to make sure you've got all the librairies installed, run  
 `pip install -r requirements.txt`

## 2. SQL database
Then you can run ***init.py*** py double-clicking on ***init.ps1*** (only do so after you checked the contents of both files, don't trust everything you got from the internet)

This will create the webtoon.sqlite database

## 3. Firefox
The program uses firefox to find the chapters on the internet, so it has to be installed. If you have issues with firefox, find the path of the executable and paste it in the "firefoxPath" property in credentials.json

## 4. Initializing the Discord bot
If you never did this, it could take a while.  
### 1. Activating developper mode  
In discord, go to User *Settings > App Settings > Advanced* and enable Developper mode.

### 2. Creating a private server
I strongly recommend that you create a custom server for yourself with a bot or manwha channel so that others aren't bothered by the bot and can't do whatever they want with your app.
### 3. Creating a bot  
Go to https://discord.com/developers.  

On the top right corner, click on the "New application" button, this will create an "application" but not a bot directly.  

Give it the name you want, accept the terms and click on create.  

Now on the left menu click on "Bot" between OAuth2 and Rich Presence.  

Here you can customize your bot name username and icon.  

When you are done with customisation, enter the bot name with its tag in the "botTag" property in credentials.json  

Then click on reset token. You'll be prompted for a 2FA code.   

Once you've entered it, click on "Copy" and paste the token the "token" property in credentials.json  

In the "Privileged Gateway Intents" category, check all 3 checkboxes : Presence Intent, Server Member Intent and Message Content Intent.  

Then click on "Save Changes".  

### 4. Inviting the bot  

Still on the same web page, got to the left menu and click on "OAuth2" and then "URL Generator".  

In the scopes table, check the "bot" scope column 2 line 6.  

In the bot permissions table, check the "Administrator" permission in the top left corner.  

Then scroll down and click on "Copy" in the bottom right corner.  

Finally open a new tab and paste the url you just copied.  

You can now add the bot to your private server.  

### 5. Settings

Send a random message in the bot channel of your server.  

Now while hovering your message click on "**...**" and then on "Copy Message Link"  

Paste the link wherever. It should start with https://discord.com/channels/ and end with 3 numbers separated by slashes.  

The first number is you guild id (it represents your server). Copy it and paste it in the "guildId" property in credentials.json  

The second number is the id of your bot channel. Copy it and paste it in the "channelId" property in credentials.json  

### 6. Optional
  
By default the commands of your bot start with a "!", but you can change in by changing the "prefix" property in credentials.json

All the documentation on discord.py is available on https://discordpy.readthedocs.io/en/stable/api.html  

## Bonus 1 : Automate (WIP)
## Bonus 2 : Kustom Widget (WIP)

## Bonus 3 : Kustom Widget (WIP)

# How it works
1. webscraping
2. SQL magic
3. Discord bot
# File description
## Python files
main.py : main program that runs the Discord Bot  

init.py : file to run before first use  

sql.py : library to interact with sqlite databases using sqlite3 by *me*  

webtoonscraping.py : file to run periodically which scraps the internet to find the chapters  


## Generated files  
webtoon.sqlite : database with all your webtoon data  

main.ps1 : allows the bot to be launched on startup  

main.cmd : this file will be generated among your computer startup processes to run main.ps1 on startup. You can find the file by pressing *Windows+R* and then launching the command *shell:startup*  

## Other files
credentials.json : file to store your credentials for portability  

init.ps1 : file that launches init.py with a double click  

requirements.txt : python librairies used  

geckodriver.exe : program that links python and Firefox  

