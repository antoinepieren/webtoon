from sql import *
from selenium.webdriver.common.by import By

NUMBERS = list("0123456789") # Pretty useful list of numbers

#_____________Functions________________
def getpath(element,path):
	liste = path.split("/")
	if len(liste) == 1:
		return element.find_element(By.XPATH,".//"+liste[0])
	return getpath(element.find_element(By.XPATH,".//"+liste[0]),"/".join(liste[1:]))

def search(l,entry):
	for i in range(len(l)):
		if l[i] == entry:
			return i
	return None

def funcsearch(l,f):
	for i in range(len(l)):
		if f(l[i]):
			return i
	return None
	
def colander(l,f):
	coL = []
	for element in l:
		if f(element):
			coL.append(element)
	return coL

def isin(elt,l):
	for elt2 in l:
		if elt == elt2:
			return True
	return False

def unify(l):
	l2 = []
	for elt in l:
		if not isin(elt,l2):
			l2.append(elt)
	return l2

def listSorting(ls): # Takes a list of lists as input
	l = ls[0]
	for i in range(len(l)):
		j=i
		while (j != 0) and (l[j-1] <= l[j]):
			l[j],l[j-1] = l[j-1],l[j]
			for k in range(1,len(ls)):
				ls[k][j],ls[k][j-1] = ls[k][j-1],ls[k][j]
			j-=1

def listGet(value,l1,l2):
	i = 0
	for i in range(len(l1)):
		if l1[i] == value:
			return l2[i]

def same(alt,main):
	n = len(request("SELECT * FROM names")) +3
	request(f"""INSERT INTO names VALUES ({n},"{main}","{alt}" """)

#printl = lambda liste : #print('\n'.join([str(x) for x in liste]))

#_______________Classes________________
class Chapter:
	def __init__(self,manwha,chaplink=None,manlink=None,chapter=None):
		self.manwha = str(manwha) # Nom du manwha
		self.manlink = str(manlink) # Lien où trouver le lien du chapitre
		self.chaplink = str(chaplink) # Lien du dernier chapitre
		self.chapter = str(chapter) # Nom du dernier chapitre
	
	def __repr__(self):
		return " - ".join([self.manwha,str(self.chapter),self.manlink,self.chaplink])
	
	def __iter__(self):
		yield str(self.manwha)
		yield str(self.chapter)
	
	def __eq__(self,other):
		return isinstance(other,self.__class__) and str(other.chapter) == str(self.chapter) and str(self.manwha) == str(other.manwha)
	
	def numerise(self): #To get a number out of a chapter name
		chapter = self.chapter
		#print(self)
		numberBool = False
		number = ""
		for c in chapter:
			if c in NUMBERS:
				number += c
				numberBool = True
			elif numberBool:
				break
		self.chapter = int(number)
	
	def values(self): #For the sql requests
		return f"""("{self.manwha}",{int(self.chapter)},"{self.chaplink}")"""
	
	def valid(self):
		return all([x != "None" for x in [str(self.manwha),str(self.chaplink),str(self.chapter)]])