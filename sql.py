"""
This library is here to help with sqlite databases
It brings the following functions :

printl (list) : prints a list in a readable manner
search (list, any) : returns the index of (any) in the list, returns None if nothing wasn't found

connect (string) : connects to a database at the path indicated by (string)
request (string) : returns the answer to the (string) request. Only works if connected to a database
table (string, list) : creates a table named (string) with the columns (list) in it, see Tutorial. Only works if connected to a database
add (string, tuple) : inserts the values (tuple) into the table (string). Only works if connected to a database
loop() : enters a loop where you can directly type requests without having to call the request function all the time. Enter whatever to cause an error and exit the loop. Only works if connected to a database
delete_column (string table, string column) : deletes the column (string column) of the table (string table). Only works if connected to a database
empty (string) : deletes every entry in the table (string) without deleting the table. Only works if connected to a database
rename (string table, string before, string after) : renames the column (string before) into (string after) in the (string table) table. Only works if connected to a database

As well as a memo at the end of the file on useful sqlite requests
Don't forget to pip install sqlite3 before using it, enjoy :)

Antoine Pieren
"""
import sqlite3
from numpy import *
from math import *

connection = None
cursor = None

printl = lambda liste : print('\n'.join([str(x) for x in liste])) # Prints a list in a readable manner

def search(l,entry):
	for i in range(len(l)):
		if l[i] == entry:
			return i
	return None

#Connect to a database
def connect(path=""):
	global connection
	global cursor
	if path:
		connection = sqlite3.connect(path)
	else:
		exec("connection = sqlite3.connect("+input()+")")
	cursor = connection.cursor()

#SQL request
def request(string):
	cursor.execute(string)
	connection.commit()
	answer = cursor.fetchall()
	return answer

def table(name,columns):
	request(f"""CREATE TABLE IF NOT EXISTS {name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {','.join(columns)});""")

def add(table,values):
	request(f"""INSERT INTO {table} VALUES {values};""")

def loop():
	flag = True
	print("Loop in")
	while flag:
		try:
			answer = request(input())
			printl([str(tup)[1:-1] for tup in answer])
		except:
			flag = False
	print("Loop out")

def delete_column(table,column):
	answer = request(f"PRAGMA table_info({table})")
	columns = [tup[1] for tup in answer]
	types = [tup[2] for tup in answer]
	i = search(columns,column)
	del columns[i]
	del types[i]
	request(f"""CREATE TABLE aux ({",".join([columns[i]+" "+types[i] for i in range(len(columns))])})""")
	request(f"""INSERT INTO aux SELECT {",".join([columns[i]+" "+types[i] for i in range(len(columns))])} FROM {table}""")
	input()
	request(f"DROP TABLE {table}")
	request(f"ALTER TABLE aux RENAME TO {table}")
	
def empty(table):
	answer = request(f"PRAGMA table_info({table})")
	columns = [tup[1] for tup in answer]
	types = [tup[2] for tup in answer]
	request(f"DROP TABLE {table}")
	request(f"""CREATE TABLE {table} ({",".join([columns[i]+" "+types[i] for i in range(len(columns))])})""")

def rename(table,before,after):
	answer = request(f"PRAGMA table_info({table})")
	columns = [tup[1] for tup in answer]
	types = [tup[2] for tup in answer]
	i = 0
	while i < len(columns):
		if columns[i] == before:
			break
		i+=1
	if i == len(columns):
		print("Mauvais nom de colonne")
	else:
		columns[i] = after
		request(f"DROP TABLE {table}")
		request(f"""CREATE TABLE {table} ({",".join([columns[i]+" "+types[i] for i in range(len(columns))])})""")
		request(f"""INSERT INTO {table} SELECT {",".join([columns[i]+" "+types[i] for i in range(len(columns))])} FROM {table}""")
	
"""
Tutorial

~~~~~~UPDATE~~~~~~
UPDATE table
SET column_1 = new_value_1,
    column_2 = new_value_2
WHERE
    search_condition 
ORDER column_or_expression
LIMIT row_count OFFSET offset;

~~~~~~INSERT~~~~~~
INSERT INTO table1 (column1,column2 ,..)
VALUES 
   (value1,value2 ,...),
   (value1,value2 ,...),
    ...
   (value1,value2 ,...);

~~~~~~DELETE~~~~~~
DELETE FROM table
WHERE search_condition;

~~~~~CREATE TABLE~~~~~
CREATE TABLE [IF NOT EXISTS] [schema_name].table_name (
	column_1 data_type PRIMARY KEY,
   	column_2 data_type NOT NULL,
	column_3 data_type DEFAULT 0,
	table_constraints
) [WITHOUT ROWID];

DROP TABLE (deletes a table)
"""
