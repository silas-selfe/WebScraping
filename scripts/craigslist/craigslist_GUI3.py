# this outputs a GUI and produces a plot with user GUI inputs

import sys
import os
from tkinter import *
from tkinter import ttk
import tkinter

import mysql.connector
import json
import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)



# restarts entire program
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


# connecting to DB
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'webscraping'
    )

cursor = mydb.cursor()



# pulling distinct cities to use in dropdown list
cityQ = "SELECT DISTINCT city FROM craigslist_forsale_us;"
#
# populating list of all cities
with mydb.cursor() as cursor:
    cursor.execute(cityQ)
    cities = cursor.fetchall()




# pulling term from db
def pullDatPlot(searchTerm):
    global avgTermPrice
    rawQuery = ["SELECT * FROM craigslist_forsale_us WHERE postTitle LIKE \'%" , searchTerm,  
    "%\' AND price > 0;"] # took out AND price < 10000

    query = "".join(rawQuery)
    with mydb.cursor() as cursor:
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())

    avgTermPrice = round(result[5].mean(),2)
    return(pd.DataFrame(result))


# taking inputs to make plot
def create_plot(searchTerm, citySelect):
    sns.set(style="white")

    # relevant df's
    raw = pullDatPlot(searchTerm)
    d1 = raw[[5]]
    d2 = raw[[5]].loc[raw[3] == citySelect]

    # set up the matplotlib figure
    f, ax = plt.subplots(1,1,figsize=(9, 5))

    # plots
    sns.kdeplot(d1.squeeze(), label="US", color='darkblue', 
        fill=True)
    sns.kdeplot(d2.squeeze(), label=citySelect, color='red',
        fill=True).set(title='Price Distribution for ' + searchTerm + '(s)' + ' in ' + citySelect)







    # Table Info
    rawTable = pullDatTab(entry.get())
    cityInfo = rawTable.loc[rawTable[0] == combo_box.get()]

    # Handling 0 search results for city
    if cityInfo.size != 0:
        cityTot = cityInfo.iat[0,1]
        cityAvg = round(cityInfo.iat[0,2],2)

        # Selecting Upper X-axis limit
        if cityAvg > avgTermPrice:
            xUpperMax = cityAvg
        else:
            xUpperMax = avgTermPrice

    else:
        cityTot = 0
        cityAvg = 0
        xUpperMax = avgTermPrice

    # Table 1 -- Search Term
    tree.insert('', 'end', text='1', values=('US', sum(rawTable[1]), avgTermPrice))
    tree.insert('', 'end', text='1', values=(combo_box.get(), cityTot, cityAvg))
    tree.place(relx=0.18, rely=0.05)

    
    topRank = rawTable.sort_values(1, ascending=False)
    botRank = rawTable.sort_values(1)

    topPrice = rawTable.sort_values(2, ascending=False)
    botPrice = rawTable.sort_values(2)
    # print(cityRankings.head())
    # print(cityRankings.iat[bottom,0])
    print(topPrice.head())

    # Table 2 -- Min/Max Posts
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[0,0], topRank.iat[0,1], round(topRank.iat[0,2],2), '|',
            topPrice.iat[0,0], topPrice.iat[0,1], round(topPrice.iat[0,2],2)))
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[1,0], topRank.iat[1,1], round(topRank.iat[1,2],2), '|',
            topPrice.iat[1,0], topPrice.iat[1,1], round(topPrice.iat[1,2],2)))
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[2,0], topRank.iat[2,1], round(topRank.iat[2,2],2), '|',
            topPrice.iat[2,0], topPrice.iat[2,1], round(topPrice.iat[2,2],2)))
    
    tree2.insert('', 'end', text='1', 
        values=('---', '---', '---', '---',
            '---', '---', '---'))

    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[2,0], botRank.iat[2,1], round(botRank.iat[2,2],2), '|',
            botPrice.iat[2,0], botPrice.iat[2,1], round(botPrice.iat[2,2],2)))
    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[1,0], botRank.iat[1,1], round(botRank.iat[1,2],2), '|',
            botPrice.iat[1,0], botPrice.iat[1,1], round(botPrice.iat[1,2],2)))
    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[0,0], botRank.iat[0,1], round(botRank.iat[0,2],2), '|',
            botPrice.iat[0,0], botPrice.iat[0,1], round(botPrice.iat[0,2],2)))
    
    
    tree2.place(relx=0.18, rely=0.72)

    # cleaning plot
    ax.legend()
    ax.set_xlim(-50, xUpperMax*3)

    ax.set(yticklabels=[])
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    # yeet
    return f



# pulling city counts for term matches
def pullDatTab(searchTerm):
    rawQuery = ["SELECT city, count(postTitle), avg(price) FROM craigslist_forsale_us " 
    "WHERE postTitle LIKE \'%" , searchTerm, "%\' AND price > 0 GROUP BY city;"]

    query = "".join(rawQuery)
    print(query)
    with mydb.cursor() as cursor:
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())

    return(pd.DataFrame(result))




# clears canvas
def _clear():
    # plot
    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)

    # this took forever to figure out
    # it clears the gray plot background making way for following plot 
    canvas.get_tk_widget().pack_forget()

    # table
    for item in tree.get_children():
        tree.delete(item)

    for item in tree2.get_children():
        tree2.delete(item)


    #tree.pack_forget()


# produces plot
def finalPlot():
    fig = create_plot(entry.get(), combo_box.get())

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)



# receiving submitted user input
def submit():
    global initial

    try: 
        initial
        _clear()
        finalPlot()
    except:
        initial = 1
        finalPlot()



#    finalPlot()

    #fill_table()
    

# deletes text in search bar
def clear():
    _clear() 

# resets search bar and drop down
def clearAll():
    entry.delete(0,END) # deletes line of text
    combo_box.set('Search')
    _clear()







# --- main ---




root = tkinter.Tk()
root.title("CraigSearch")
root.geometry("1100x950")


# buttons and placement
submit = Button(root, text="Submit", command=submit).place(relx = 0.6, rely=0.063)
clearAll = Button(root, text='Clear All', command=clearAll).place(relx = 0.65, rely=0.063)
clear = Button(root, text='Clear Graph', command=clear).place(relx = 0.6, rely=0.1)
reset = Button(root, text="Reset", command=restart_program).place(relx = 0.67, rely=0.1)

# search bar
sBar = Label(root, text='Enter search term')
sBar.pack(pady=10)
entry = Entry()
entry.pack()

# drop down menu
cityDrop = Label(root, text='Select the nearest city')
cityDrop.pack(pady=10)

# Creating CraigSearch
combo_box = ttk.Combobox(root, value=cities)
combo_box.set('Search')
combo_box.pack()





# creating table
style = ttk.Style()
style.theme_use('clam')

# treeview widget
tree = ttk.Treeview(root, column=("Location", "Search Matches", "Avg Price"), 
    show='headings', height=2)

tree.column("# 1", width=100, anchor=CENTER)
tree.heading("# 1", text="Location")
tree.column("# 2", width=60, anchor=CENTER)
tree.heading("# 2", text="Results")
tree.column("# 3", width=70, anchor=CENTER)
tree.heading("# 3", text="Avg Price")


tree2 = ttk.Treeview(root, 
    column=("Max/Min Posts (3)", "Search Matches", "Avg Price", " ",
        "Max/Min Price", "Search Matches", "Avg Price"), 
    show='headings', height=7)

tree2.column("# 1", width=120, anchor=CENTER)
tree2.heading("# 1", text="Max/Min Posts (3)")
tree2.column("# 2", width=50, anchor=CENTER)
tree2.heading("# 2", text="Posts")
tree2.column("# 3", width=60, anchor=CENTER)
tree2.heading("# 3", text="Avg Price")

tree2.column("# 4", width=30, anchor=CENTER)
tree2.heading("# 4", text="  ")

tree2.column("# 5", width=100, anchor=CENTER)
tree2.heading("# 5", text="Max/Min Price")
tree2.column("# 6", width=50, anchor=CENTER)
tree2.heading("# 6", text="Posts")
tree2.column("# 7", width=60, anchor=CENTER)
tree2.heading("# 7", text="Avg Price")

# Insert data into widget
# tree.insert('', 'end', text='1', values=('US', 1234, 123))
# tree.insert('', 'end', text='1', values=(combo_box.get(), 334, 34))

#tree.place(relx=0.1, rely=0.8)







# initializing GUI
tkinter.mainloop()




# widget placement
# https://www.pythontutorial.net/tkinter/tkinter-place/