"""
This program is the main loop of the project that will run the discord bot.
It revolves around a single class called Main inheriting from discord.client().
The routines defined in discord.py are overriden by the methods defined in Main, and that's how a discord bot works
"""
import discord # Discord python API
import json # Used to safely store and recover personnal data that won't be shared on github
from functions import * # Useful functions
from time import sleep # Needed for timers
import subprocess # Used to launch webtoon scraping at regular intervals
import threading # Used to generate regular intervals

#_________________Settings____________________

# Getting bot data from credentials.json
file = open("credentials.json",'r')
data = json.load(file)
file.close()

token = data["token"] # Bot token
guildId = data["guildId"] # Server Id
channelId = data["channelId"] # Id of the channel in which the bot should work in priority
p = data["prefix"] # Charchter to indicate a command
botTag = data["botTag"] # Tag of the bot to remember so that the bot doesn't respond to itself

intents = discord.Intents.all() # I put all() because I'm too lazy to try and understand this
delay = 3 # Delay for website to load
chapterList = [] # List that will contain all the chapters on all websites

#_______________Discord client__________________

class Main(discord.Client):
	startFlag = True # Boolean that stops initialisation from happening multiple times
	processes = [] # List of processes, used for launching the scraping program
	threads = [] # List of threads, used here for the hour-long loop between scrapings
	
	async def on_message(self,message):
		if str(message.author) == botTag or message.guild != self.guild: # Safety condition
			pass
		else:
			if message.content == p+"ping": # Function to check if the bot is connected from discord
				await message.channel.send("pong")

			elif message.content == p+"close": # Stops the bot
				await message.channel.send("Bot offline")
				await client.close()

			elif message.content == p+"toread":
				answer = request("""SELECT names.main,chapter,link,last_out,last_read FROM (SELECT title,last_read FROM list WHERE last_out-last_read != 0 AND interest="READING" AND status="ONGOING") AS new JOIN chapters ON chapters.title = new.title JOIN names ON chapters.title = names.alt WHERE chapter-last_read > 0""") # THE sql request
				# Removing Duplicates
				chapterList = []
				for tup in answer:
					if tup not in chapterList:
						if any([tup[0] == chapter[0] for chapter in chapterList]):
							i = funcsearch(chapterList,lambda x : x[0] == tup[0])
							if int(tup[1]) < int(chapterList[i][1]):
								chapterList.append(tup)
						else:
							chapterList.append(tup)
				if len(chapterList) == 0:
					await message.channel.send("Nothing new to read")
				else:
					
					await message.channel.send(f"Here are the chapters you haven't read yet ({len(chapterList)})")
					for chapter in chapterList :
						string = f"{chapter[0]} Chapter {chapter[1]} : <{chapter[2]}> ({chapter[1] - chapter[4] + 1} {chapter[3] - chapter[4]})" # The <> are used to remove the automatic embed when sending a link in Discord, the rest is explained in the README.MD
						mes = await message.channel.send(string)
						await mes.add_reaction("\U0001F4D6") # "Open book" emoji
						await mes.add_reaction("\U0001F61B") # "Prohibited" emoji

	#___________Discord bot Initialisation_________
	async def on_ready(self):
		if self.startFlag: # Ensures initialisation is only executed once
			self.startFlag = False

			self.guild = client.get_guild(guildId) # Your discord server
			self.channel = self.guild.get_channel(channelId) # Main channel for the bot to write in
			await self.channel.send("Bot online")
			self.loop.create_task(self.process_loop())
			print("Mise en ligne du bot OK")
			process = subprocess.Popen(["python.exe", "webtoonscraping.py"])
			self.processes.append(("scraping",process,None))
			thread = threading.Thread(target = lambda : sleep(3600))
			thread.start()
			self.threads.append(("loop",thread))
	
	#_________Message reactions processing_________
	async def on_raw_reaction_add(self,payload):
		if str(payload.member) != botTag:
			if payload.emoji.name == "\U0001F4D6" : # Open book emoji
				channel = self.guild.get_channel_or_thread(payload.channel_id)
				message = await channel.fetch_message(payload.message_id)
				liste = message.content.split("Chapter")
				title = spaceremove(liste[0])
				chapter = int(liste[1].split(":")[0])
				last_read = request(f"""SELECT last_read FROM list WHERE title = "{title}" """)[0][0]
				last_out = request(f"""SELECT last_out FROM list WHERE title = "{title}" """)[0][0]
				if int(chapter) > int(last_read): # Updating last_read
					request(f"""UPDATE list SET last_read = {chapter} WHERE title = "{title}" """)
				if int(chapter) < int(last_out): # Editing message if a new chapter has already been found for this webtoon
					# TODO : upgrade the following line 'cause it always give errors 
					next_out = request(f"""SELECT min(chapter),link FROM chapters WHERE title = "{title}" AND chapter > "{int(chapter)}" """)[0]
					answer = request(f"""SELECT link FROM chapters WHERE title = "{title}" AND chapter="{int(chapter)+1}" """)[0][0]
					#string = f"{title} Chapter {int(chapter)+1} : <{answer}>"
					string = f"{title} Chapter {next_out[0]} : <{next_out[1]}> ({int(next_out[0]) - int(chapter) + 1} {last_out - int(chapter)})"
					await message.edit(content = string)
					await message.remove_reaction(payload.emoji,payload.member)
				else:
					await message.delete()
		# TODO : Unauthorized emoji

#_______________Initialisation________________
connect("webtoon.sqlite") #Connecting to sql database

counter = 1
while counter < 5:
	try:
		client = Main(intents=intents)
		client.run(token) # Starting Event Loop
	except:
		del client
		print(f"Connection failed, retrying in {10*counter} seconds")
		sleep(10*counter)
		counter += 1

# TODO : write this in the json comments in the readme :
"""
This json file is made to store your credentials and other bot properties that probably shouldn't be on github
Be careful with your data, discord searches for and blocks bots whose token is on the internet.
Besides, these informations could help people hack you.
Here are the infos in the json file
token : your bot token generated in developper.discord.com
"""
