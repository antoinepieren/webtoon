# Installation
## 1. Python librairies
First of all, to make sure you've got all the librairies installed, run  
 `pip install -r requirements.txt`

## 2. SQL database
Then you can run ***init.py*** py double-clicking on ***init.ps1*** (only do so after you checked the contents of both files, don't trust everything you got from the internet)

This will create the webtoon.sqlite database

## 3. Firefox
The program uses firefox to find the chapters on the internet, so it has to be installed.

## 4. Initializing the Discord bot
If you never did this, it could take a while.  
// TODO : Discord bot setup tutorial with json file and all  
// TODO : How to do hyperlinks in markdown for Bonus sections

## Bonus 1 : Automate
## Bonus 2 : Kustom Widget

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

## Other files
credentials.json : file to store your credentials for portability  
init.ps1 : file that launches init.py with a double click  
requirements.txt : python librairies used  
geckodriver.exe : program that links python and Firefox
