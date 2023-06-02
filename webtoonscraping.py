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

	
service = Service(executable_path="geckodriver.exe") # TODO : test if necessary
firoptions = webdriver.FirefoxOptions()
#firoptions.add_argument('--headless') # Unquote this line to let the program work in the background
try:
	driver = webdriver.Firefox(options=firoptions,service=service)#Connecting to the Internet
except:
	file = open("credentials.json",'r')
	data = json.load(file)
	file.close()
	if data["firefoxPath"] :
		firoptions.binary_location = data["firefoxPath"]
		driver = webdriver.Firefox(options=firoptions,service=service)#Connecting to the Internet
	else:
		try:
			firoptions.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
			driver = webdriver.Firefox(options=firoptions,service=service)#Connecting to the Internet
		except:
			print("Firefox isn't correctly detected by the program, please fill the \"firefoxPath\" value of credentials.json with the path to the Firefox executable")
wait = WebDriverWait(driver, delay)


#_____________Asura Scans______________21

asuraList = []
#Page loading
try:
	driver.get("https://www.asurascans.com/")
	sleep(5)
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="bixbox"]'))
	test = wait.until(element_present) # Waiting for page to load
	#button = driver.find_element(By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
	#button.click()
	#sleep(1)
	
	try:
		latest = driver.find_element(By.XPATH, '//div[@class="bixbox"]')
		divList = driver.find_elements(By.XPATH, '//div[@class="luf"]') # Locating all new chapters
		#Adding all chapters as Chapter class variables in chapterList
		sleep(5)
		for div in divList:
			manwha = div.find_element(By.XPATH,".//a").get_attribute("title")
			if "Discord" in manwha:
				continue
			manlink = div.find_element(By.XPATH,".//a").get_attribute("href")
			chapter = div.find_element(By.XPATH,'.//li/a').text
			chaplink = div.find_element(By.XPATH,'.//li/a').get_attribute("href")
			chapter = Chapter(manwha,chapter=chapter,manlink=manlink)
			print(chapter)
			try:
				chapter.numerise()
				asuraList.append(chapter)
			except:
				pass
	except:
		pass
except:
	pass

'''
#Finding chapter links
for chapter in asuraList:
	try:
		driver.get(chapter.manlink)
		element_present = ec.presence_of_all_elements_located((By.XPATH,'//ul[@class="clstyle"]'))
		test = wait.until(element_present) # Waiting for page to load
		ul = driver.find_element(By.XPATH,'//ul[@class="clstyle"]')
		lilist = ul.find_elements(By.XPATH,'.//li')
		li = lilist[funcsearch(lilist,lambda x:str(chapter.chapter) in str(x.get_attribute("data-num")))]
		chapter.chaplink = li.find_element(By.XPATH,'.//a').get_attribute("href")
	except:
		#print(f"Error with {chapter}")
		del chapter
'''

chapterList += asuraList

#___________Reaper Scans_______________1
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

#___________Flame Scans_______________1

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

#___________Luminous Scans_______________21

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
			print(chapter)
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

#___________Mm Scans_______________1

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
			print(chapter)
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
			print(chapter)
			try:
				chapter.numerise()
				chapterList.append(chapter)
			except:
				print("num error")
				pass
	except:
		pass
except:
	pass

#_______________END____________________
# Never forget to quit the driver at the end
driver.close()

length = len(chapterList)
i = 0
while i < length:
	if chapterList[i].valid():
		i+=1
	else:
		del chapterList[i]


connect("webtoon.sqlite")
data = request("SELECT * FROM names")
mains = [line[0] for line in data]
alts = [line[1] for line in data]


#print("\n\nNew Manwhas\n")
file = open("buffer","a")
length = len(chapterList)
i = 0
while i < length:
	chapter = chapterList[i]
	if chapter.manwha in alts:
		chapter.manwha = listGet(chapter.manwha,alts,mains)
		i += 1
	else:
		if chapter.manwha != "":
			file.write(str(chapter)+"\n")
			#print(chapter)
			request(f"""INSERT INTO list VALUES ("{chapter.manwha}","NOT CHECKED","ONGOING",{int(chapter.chapter)},0)""")
			request(f"""INSERT INTO chapters VALUES ("{chapter.manwha}",{int(chapter.chapter)},"{chapter.chaplink}")""")
			request(f"""INSERT INTO names VALUES ("{chapter.manwha}","{chapter.manwha}")""")
		del chapterList[i]
		length -= 1
file.close()

chapterList = unify(chapterList)

chapters = [(chapter[0],chapter[1]) for chapter in request("SELECT * FROM chapters")]
for chapter in chapterList:
	if not isin(tuple(chapter),chapters):
		print(chapter)
		request(f"INSERT INTO chapters VALUES {chapter.values()}")
		last_out = request(f"""SELECT last_out FROM list WHERE title = "{chapter.manwha}" """)[0][0]
		if last_out < int(chapter.chapter):
			request(f"""UPDATE list SET last_out = {int(chapter.chapter)}, status = "ONGOING" WHERE title = "{chapter.manwha}" """)
	