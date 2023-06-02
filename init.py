from sql import *

# TODO : Check if empty with SELECT name FROM sqlite_schema WHERE type='table'
connect("webtoon.sqlite") # Creating database if it doesn't exist yet
#request("DROP TABLE names")
request("CREATE TABLE names (id INT PRIMARY KEY,main TEXT,alt TEXT)") # Table for webtoon with multiple names because of translation
request("CREATE TABLE list (id INT PRIMARY KEY,title TEXT,interest TEXT,status TEXT,last_out INT,last_read INT)") # Table for the list of different webtoons and their charachteristics
request("CREATE TABLE chapters (id INT PRIMARY KEY,title TEXT,chapter INT,link TEXT)") # Table for all the chapters detected