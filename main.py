"""
This program is the main loop of the project that will run the discord bot.
It revolves around a single class called Main inheriting from discord.client().
The routines defined in discord.py are overriden by the methods defined in Main, and that's how a discord bot works
"""
import discord
import json

# Getting bot data from credentials.json
file = open("credentials.json",'r')
data = json.load(file)
file.close()

token = data["token"] # Bot token
guildId = data["guildId"] # Server Id
channelId = data["channelId"] # Id of the channel in which the bot should work in priority
p = data["prefix"] # Charchter to indicate a command

intents = discord.Intents.all() # I put all() because I'm too lazy to try and understand this
delay = 3 # Delay for website to load
NUMBERS = list("0123456789") # Pretty useful list of numbers
chapterList = [] # List that will contain all the chapters on all websites

# TODO : write this in the json comments in the readme :
"""
This json file is made to store your credentials and other bot properties that probably shouldn't be on github
Be careful with your data, discord searches for and blocks bots whose token is on the internet.
Besides, these informations could help people hack you.
Here are the infos in the json file
token : your bot token generated in developper.discord.com
"""
