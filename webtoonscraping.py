from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.service import Service
from sql import *
from time import sleep,time
import json
from functions import *

delay = 3 # Delay for website to load
NUMBERS = list("0123456789") # Pretty useful list of numbers
chapterList = [] # List that will contain all the chapters on all websites

	
service = Service(executable_path="geckodriver.exe") # Selenium firefox service object
firoptions = webdriver.FirefoxOptions() # Webdriver options
firoptions.add_argument('--headless') # Unquote this line to let the program work in the background

try:
	driver = webdriver.Firefox(options=firoptions,service=service) # Connecting to the Internet
except:
	file = open("credentials.json",'r')
	data = json.load(file)
	file.close()
	if data["firefoxPath"] :
		firoptions.binary_location = data["firefoxPath"]
		driver = webdriver.Firefox(options=firoptions,service=service) # Connecting to the Internet with custom Firefox path
	else:
		try:
			firoptions.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
			driver = webdriver.Firefox(options=firoptions,service=service) # Connecting to the Internet with usual Firefox path
		except:
			print("Firefox isn't correctly detected by the program, please fill the \"firefoxPath\" value of credentials.json with the path to the Firefox executable")
wait = WebDriverWait(driver, delay)

#______Scraping different websites_____

#_____________Asura Scans______________

asuraList = []
# Page loading
try:
	driver.get("https://www.asurascans.com/")
	sleep(5)
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="bixbox"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	try:
		latest = driver.find_element(By.XPATH, '//div[@class="bixbox"]')
		divList = latest.find_elements(By.XPATH, './/div[@class="luf"]') # Locating all new chapters
		#Adding all chapters as Chapter class variables in chapterList
		sleep(5)
		for div in divList:
			manwha = div.find_element(By.XPATH,".//a").get_attribute("title")
			if "Discord" in manwha:
				continue
			manlink = div.find_element(By.XPATH,".//a").get_attribute("href")
			chapter = div.find_element(By.XPATH,'.//li/a').text
			chaplink = div.find_element(By.XPATH,'.//li/a').get_attribute("href")
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				asuraList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass

chapterList += asuraList

#___________Reaper Scans_______________

try:
	driver.get("https://reaperscans.com/latest/comics")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="focus:outline-none"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	try:
		divList = driver.find_elements(By.XPATH, '//div[@class="focus:outline-none"]') # Locating all new chapters
		#Adding all chapters as Chapter class variables in chapterList
		for div in divList:
			manwha = ""
			start = time()
			while manwha == "":
				aList = div.find_elements(By.XPATH,'.//a')
				manwha = aList[0].text
				if time()-start > 10:
					break
			manlink = aList[0].get_attribute("href")
			chaplink = aList[1].get_attribute("href")
			chapter = chaplink.split("-")[-1]
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass

#___________Flame Scans_______________

try:
	driver.get("https://flamescans.org/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="bs styletere"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	latest = driver.find_element(By.XPATH, '//div[@class="latest-updates"]')
	try:
		divList = latest.find_elements(By.XPATH, './/div[@class="bs styletere"]') # Locating all new chapters
		#Adding all chapters as Chapter class variables in chapterList
		for div in divList:
			info = div.find_element(By.XPATH,'.//div[@class="info"]')
			chaps = div.find_element(By.XPATH,'.//div[@class="chapter-list"]')
			manwha = info.find_element(By.XPATH,'.//div[@class="tt"]').text
			chapter = chaps.find_element(By.XPATH,'.//div[@class="epxs"]').text
			manlink = info.find_element(By.XPATH,".//a").get_attribute("href")
			chaplink = chaps.find_element(By.XPATH,'.//a').get_attribute("href")
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass

#____________Luminous Scans______________

luminousList = []
try:
	driver.get("https://luminousscans.com")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]'))
	test = wait.until(element_present) # Waiting for page to load
	button = driver.find_element(By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
	button.click()
	sleep(1)
	
	try:
		divList = driver.find_elements(By.XPATH, '//div[@class="luf"]') # Locating all new chapters	
		#Adding all chapters as Chapter class variables in chapterList
		for div in divList:
			aList = div.find_elements(By.XPATH, './/a')
			manwha = aList[0].text
			manlink= aList[0].get_attribute("href")
			chapter = aList[1].text
			chaplink = aList[1].get_attribute("href")
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				luminousList.append(chapter)
			except:
				#print("1")
				pass
	except:
		#print("2")
		pass
except:
	#print("3")
	pass

chapterList += luminousList

#___________Mm Scans_______________
# TODO : Fix this shit but damn I hate it
try:
	driver.get("https://mm-scans.org/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="page-item-detail"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	
	latest = driver.find_element(By.XPATH,'//div[@class="lastest-content"]')
	try:
		divList = latest.find_elements(By.XPATH, './/div[@class="page-item-detail"]') # Locating all new chapters
		#Adding all chapters as Chapter class variables in chapterList
		for div in divList:
			main = div.find_element(By.XPATH,'.//div[@class="item-thumb"]')
			aList = main.find_elements(By.XPATH,".//a")
			manwha = aList[0].get_attribute("title")
			chapter = aList[1].text
			manlink = aList[0].get_attribute("href")
			chaplink = aList[1].get_attribute("href")
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass


#____________Zero Scans________________
try:
	driver.get("https://zeroscans.com/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="d-flex flex-column justify-center py-2"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	try:
		divList = driver.find_elements(By.XPATH, '//div[@class="d-flex flex-column justify-center py-2"]')
		for div in divList:
			aList = div.find_elements(By.XPATH,".//a")
			manlink = aList[0].get_attribute("href")
			manwha = div.find_element(By.XPATH,'.//div[@class="text-left text-capitalize text-truncate"]').text
			chaplink = aList[1].get_attribute("href")
			chapter = aList[1].find_element(By.XPATH,'.//div[@class="text-body-2 relative"]').text
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				#print("num error")
				pass
	except:
		pass
except:
	pass

#____________Aqua Manga________________
try:
	driver.get("https://aquamanga.com/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="item-summary"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	try:
		divList = driver.find_elements(By.XPATH, '//div[@class="item-summary"]')
		for div in divList:
			aList = div.find_elements(By.XPATH,".//a")
			manlink = aList[0].get_attribute("href")
			manwha = aList[0].text
			chaplink = aList[1].get_attribute("href")
			chapter = aList[1].text
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			#print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				#print("num error")
				pass
	except:
		pass
except:
	pass

#____________Manga Gecko________________
try:
	driver.get("https://www.mangageko.com/jumbo/manga/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="novel-item"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	try:
		divList = driver.find_elements(By.XPATH, '//li[@class="novel-item]')
		for div in divList:
			manwha = div.find_element(By.XPATH,'.//h4').text
			chapter = spaceremove(div.find_element(By.XPATH,'.//h5').text)
			manlink = div.find_element(By.XPATH,'.//a').get_attribute("href")
			chaplink = "https://www.mangageko.com/reader/en/" + manlink.split('/')[1] + "-chapter-" + chapter.split(" ")[1]
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink,chaplink=chaplink)
			print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass


#__________Webscraping end_____________
# Never forget to quit the driver at the end
driver.close()

#_______Sqlite database update_________

# Removing incomplete chapters
length = len(chapterList)
#print(f"********************\n Printing chapterlist right after webscraping with length {length}\n********************************\n\n")
#printl(chapterList)
sleep(1)
i = 0
while i < length:
	if chapterList[i].valid():
		i+=1
	else:
		del chapterList[i]
		length-=1

# Getting data from database
connect("webtoon.sqlite")
data = request("SELECT * FROM names")
mains = [line[1] for line in data] # List of main names of webtoons
alts = [line[2] for line in data] # List of alternative names of webtoons 
chapterId = len(request("SELECT * FROM chapters")) # Number of chapters
listId = len(request("SELECT * FROM list")) # Number of webtoons
nameId = len(data) # Number of webtoon names

#print(f"********************\n Printing chapters from new webtoons\n********************************\n\n")
# Adding new webtoons
length = len(chapterList)
i = 0
while i < length:
	chapter = chapterList[i]
	if chapter.manwha in alts: # Checking if the webtoon already exists
		chapter.manwha = listGet(chapter.manwha,alts,mains) # Getting the webtoon's main name
		i += 1
	else:
		if chapter.manwha != "": # Sometimes there are empty manwha names
			#print(chapter)
			request(f"""INSERT INTO list VALUES ({listId},"{chapter.manwha}","NOT CHECKED","ONGOING",{int(chapter.chapter)},0)""")
			request(f"""INSERT INTO chapters VALUES ({chapterId},"{chapter.manwha}",{int(chapter.chapter)},"{chapter.chaplink}",1)""")
			request(f"""INSERT INTO names VALUES ({nameId},"{chapter.manwha}","{chapter.manwha}")""")
			listId += 1
			chapterId += 1
			nameId += 1
		del chapterList[i]
		length -= 1

chapterList = unify(chapterList) # Chapter unicity function
#print(f"********************\n Printing chapterlist right after unify with length {len(chapterList)}\n********************************\n\n")
#printl(chapterList)
sleep(1)

chapters = request("SELECT title,chapter FROM chapters") # List of chapters, including those of new webtoons
# Adding new chapters
#print(f"********************\n Printing new chapters\n********************************\n\n")
for chapter in chapterList:
	if not isin(tuple(chapter),chapters):
		#print(chapter)
		request(f"INSERT INTO chapters VALUES ({chapterId},{chapter.values()},1)")
		chapterId += 1

		# Changing last_out
		last_out = request(f"""SELECT last_out FROM list WHERE title = "{chapter.manwha}" """)[0][0]
		if last_out < int(chapter.chapter): 
			request(f"""UPDATE list SET last_out = {int(chapter.chapter)}, status = "ONGOING" WHERE title = "{chapter.manwha}" """)