from sql import *
import subprocess

connect("webtoon.sqlite") # Creating database if it doesn't exist yet
request("CREATE TABLE names (id INT PRIMARY KEY,main TEXT,alt TEXT)") # Table for webtoon with multiple names because of translation
request("CREATE TABLE list (id INT PRIMARY KEY,title TEXT,interest TEXT,status TEXT,last_out INT,last_read INT)") # Table for the list of different webtoons and their charachteristics
request("CREATE TABLE chapters (id INT PRIMARY KEY,title TEXT,chapter INT,link TEXT, valid INT)") # Table for all the chapters detected

process = subprocess.Popen(["powershell.exe","pwd"],stdout=subprocess.PIPE)
out, err = process.communicate()
path = str(out)[2:-1].replace("\\r\\n","\n")[85:-3].replace("\\\\","\\") # Current directory
startPath = "\\".join(path.split('\\')[:3]) + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" # Startup programs directory
file = open(startPath + "\\main.cmd", "w")
file.write(f"START /B \"\" {path}\\main.ps1") # This will make the bot run at startup
file.close()
file = open(path + "\\main.ps1", "w")
file.write(f"cd {path}\n")
file.write("python.exe main.py")
file.close()
