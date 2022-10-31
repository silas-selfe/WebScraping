# import mysql.connector
# import json
# import math
# import statistics
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# import numpy as np



# mydb = mysql.connector.connect(
# 	host = 'localhost',
# 	user = 'root',
# 	password = '1234',
# 	database = 'webscraping'
# 	)

# cursor = mydb.cursor()


# searchInput = 'tool'
# locationSelection = 'altoona'
# #searchInput = input("\nTerm: ")



# # combining query with input search term
# rawQuery = ["SELECT * FROM craigslist_forsale_us WHERE postTitle LIKE \'% " , searchInput,  
# 	"%\' AND price > 0 AND price <= 10000;"]
# query = "".join(rawQuery)

# #print(query)
# with mydb.cursor() as cursor:
# 	cursor.execute(query)
# 	result = pd.DataFrame(cursor.fetchall())

# df = pd.DataFrame(result)
# dfPlace = df.loc[df[3] == locationSelection]



# curPrice = df[[5]]
# curPriceLoc = dfPlace[[5]]


# if statistics.stdev(curPrice[5]) < len(curPrice):
# 	binCount = statistics.stdev(curPrice[5])# / min(curPrice[5])
# else:
# 	binCount = len(curPrice)# / min(curPrice[5])

# test = sns.distplot(curPrice, hist=True, kde=False, 
# 	bins=round(binCount), color='darkblue', label="US",
# 	hist_kws={'edgecolor':'black'},
# 	kde_kws = {'linewidth':1})

# test2 = sns.distplot(curPriceLoc, hist=True, kde=False, 
# 	bins=round(25), color='red', label = locationSelection,
# 	hist_kws={'edgecolor':'black'},
# 	kde_kws = {'linewidth':1})

# test.set_xlim(0,np.percentile(curPrice, 90))
# test.set_xlabel("Price ($)")
# test.set_ylabel("Frequency")
# test.set_title("Price Distribution for " + searchInput + '(s)')


# plt.legend()
# plt.show()




# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Create an object of Style widget
style = ttk.Style()
style.theme_use('clam')

# Add a Treeview widget
tree = ttk.Treeview(win, 
	column=("FName", "LName", "Roll No"),
	row=("One", "Two")
	show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="FName")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="LName")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="Roll No")

# Insert the data in Treeview widget
tree.insert('', 'end', text="1", values=('Amit', 'Kumar', '17701'))
tree.insert('', 'end', text="1", values=('Ankush', 'Mathur', '17702'))
tree.insert('', 'end', text="1", values=('Manisha', 'Joshi', '17703'))
tree.insert('', 'end', text="1", values=('Shivam', 'Mehrotra', '17704'))

#tree.pack()
tree.place(relx=0.1, rely=0.5)


# win.mainloop()










# vehicles = ['atv/utv/sno', 'auto parts', 'aviation', 'boat parts', 'boats', 'cars+trucks', 'heavy equip', 'motorcycles', 'motorcycle parts', 'trailers', 'wheels+tires']
# vAbbr = ['sna', 'pta', 'ava', 'bpa', 'boo', 'cta', 'hva', 'mca', 'mpa', 'tra', 'wta']

# outdoors = ['bikes', 'bike parts', 'farm+garden', 'rvs+camp', 'sporting', 'tickets']
# oAbbr = ['bia', 'bip', 'gra', 'rva', 'sga', 'tia']

# home = ['antiques', 'appliances', 'baby+kid', 'beauty+hlth', 'books', 'cds/dvd/vhs', 'clothes+acc', 'collectibles', 'furniture', 'household', 'jewelry', 'tools']
# homeAbbr = ['ata', 'ppa', 'baa', 'haa', 'bka', 'ema', 'cla', 'cba', 'fua', 'hsa', 'jwa', 'tla']

# computer = ['computer parts', 'computers', 'electronics', 'cell phones']
# cAbbr = ['syp', 'sya', 'ela', 'moa']

# hobbies = ['arts+crafts', 'music instr', 'photo+video', 'toys+games', 'video gaming']
# hAbbr = ['ara', 'msa', 'pha', 'taa', 'vga']


