from sql import *

connect("webtoon.sqlite") # Creating database if it doesn't exist yet
#request("DROP TABLE names")
request("CREATE TABLE names (id INT PRIMARY KEY,main TEXT,alt TEXT)") # Table for webtoon with multiple names because of translation
request("CREATE TABLE list (title TEXT,interest TEXT,status TEXT,last_out INT,last_read INT)")