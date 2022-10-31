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



def pullDat(searchTerm):
    rawQuery = ["SELECT * FROM craigslist_forsale_us WHERE postTitle LIKE \'% " , searchTerm,  
    "%\' AND price > 0 AND price <= 10000;"]
    query = "".join(rawQuery)

    with mydb.cursor() as cursor:
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())

    return(pd.DataFrame(result))




def create_plot(searchTerm, citySelect):
    sns.set(style="white")

    # Generate a large random dataset
    raw = pullDat(searchTerm)
    d1 = raw[[5]]
    d2 = raw[[5]].loc[raw[3] == citySelect]

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(5, 5))

    # Generate a custom diverging colormap
    sns.kdeplot(d1.squeeze(), label="US", color='darkblue', 
        fill=True)
    sns.kdeplot(d2.squeeze(), label=citySelect, color='red',
        fill=True).set(title='Price Distribution for ' + searchTerm + '(s)')

    # sns.distplot(d1.squeeze(), kde=True, label="US", color='darkblue',
    #    hist_kws={'edgecolor':'black'})
    # sns.distplot(d2.squeeze(), kde=True, label=citySelect, color='red',
    #    hist_kws={'edgecolor':'black'})

    ax.legend()
    ax.set_xlim(-50, 4000)
    ax.set(yticklabels=[])
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    #plt.set(yticklabels=[])
    
    return f


def finalPlot(searchTerm, citySelect):
    fig = create_plot(searchTerm, citySelect)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()


# taking search bar and dropdown selection as inputs
def submit():
    searchTerm = entry.get()
    citySelect = combo_box.get()

    finalPlot(searchTerm, citySelect)

# deletes text in search bar
def clear():
    entry.delete(0,END) 

# resets search bar and drop down
def clearAll():
    entry.delete(0,END) # deletes line of text
    combo_box.set('Search')



# --- main ---
root = tkinter.Tk()
root.title("CraigSearch")
root.geometry("500x500")


# search and clear buttons with placement
submit = Button(root, text="Submit", command=submit)
clear = Button(root, text='Clear', command=clear)
clearAll = Button(root, text='Clear All', command=clearAll)
submit.pack(side=RIGHT)
clear.pack(side=RIGHT)
clearAll.pack(side=RIGHT)

# search bar
sBar = Label(root, text='Enter search term')
sBar.pack()
entry = Entry()
entry.pack()

# drop down menu
cityDrop = Label(root, text='Select the nearest city')
cityDrop.pack()

# Creating CraigSearch
combo_box = ttk.Combobox(root, value=cities)
combo_box.set('Search')
combo_box.pack()

# initializing GUI
tkinter.mainloop()