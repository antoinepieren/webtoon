"""
This program allows you to interact with the program and customize it.
"""

from tkinter import * # GUI python library
from tkinter import ttk # Used for styling the GUI
from sql import * # Sql library made by me to make the sqlite3 library easier to use

connect("webtoon.sqlite") # Connecting to the database
statuses = ["READ","READING","NOT INTERESTED","NOT CHECKED"] # Different statuses possible for webtoons
nameSize = 100 # Maximum length of a webtoon name

class Main(Tk):
	def __init__(self):
		Tk.__init__(self) # Initialisation
		self.geometry("1920x1080") # Window size
		self.title("Webtoon GUI") # Window title

		# Tabs
		self.notebook = ttk.Notebook(self)
		self.frames = {}

		frame1 = Frame(self.notebook)
		self.frames["Interest"] = frame1
		self.notebook.add(frame1, text="Interest")

		frame2 = Frame(self.notebook)
		self.frames["Naming"] = frame2
		self.notebook.add(frame2, text="Naming")

		self.notebook.pack(expand = 1, fill ="both")

		# Interest content
		# Webtoon selection
		left = Frame(self.frames["Interest"])
		left.grid(column=0,row=0)

		self.webtoonList = [x[0] for x in request("SELECT DISTINCT title FROM list ORDER BY title")]
		var = Variable(value=self.webtoonList)
		self.listbox = Listbox(left,listvariable=var,height=50,width=nameSize,selectmode="single")
		self.listbox.grid(column=1,row=0)
		scrollbar = Scrollbar(left,orient=VERTICAL,command=self.listbox.yview)
		self.listbox['yscrollcommand'] = scrollbar.set
		scrollbar.grid(column=0,row=0,sticky=N+S)
		self.listbox.bind('<<ListboxSelect>>',self.select)

		# Webtoon interest changing
		right = Frame(self.frames["Interest"])
		right.grid(column=1,row=0)

		self.titleLabel = Label(right,text="Select a webtoon")
		self.titleLabel.grid(column=0,row=0)
		
		Label(right,text="Current interest :").grid(column=0,row=1)

		self.interestLabel = Label(right,text="")
		self.interestLabel.grid(column=0,row=2)

		self.statusSelection = StringVar()
		self.statusSelection.set(statuses[0])
		selectStatus = OptionMenu(right, self.statusSelection, *statuses)
		selectStatus.grid(column=0,row=3)

		statusButton = Button(right,text="Change", command=self.changeStatus,padx=0,pady=0)
		statusButton.grid(column=0,row=4)




		# Naming content
		Label(self.frames["Naming"], text="WIP").pack()
	
	def select(self,event):
		index = self.listbox.curselection()[0]
		self.titleLabel.configure(text=self.webtoonList[index])
		self.interestLabel.configure(text=request(f"SELECT interest FROM list WHERE title=\"{self.webtoonList[index]}\" ")[0][0])
	
	def changeStatus(self):
		index = self.listbox.curselection()[0]
		request(f"UPDATE list SET interest=\"{self.statusSelection.get()}\" WHERE title=\"{self.webtoonList[index]}\" ")
		self.select(None)
	

		

main = Main()
main.mainloop()


