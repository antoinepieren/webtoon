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
#firoptions.add_argument('--headless') # Unquote this line to let the program work in the background

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

#___________Mm Scans_______________

try:
	driver.get("https://mm-scans.org/")
	element_present = ec.presence_of_all_elements_located((By.XPATH, '//div[@class="page-item-detail"]'))
	test = wait.until(element_present) # Waiting for page to load
	
	sleep(3)
	button = driver.find_element(By.XPATH,'//button[@class="fc-button fc-cta-consent fc-primary-button"]')
	button.click()
	sleep(1)
	driver.close()
	sleep(1)
	button = driver.find_element(By.XPATH,'//button[@class="fc-button fc-cta-consent fc-primary-button"]')
	button.click()
	sleep(1)
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

driver.close()
