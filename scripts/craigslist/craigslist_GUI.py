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



def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
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
def pullDat(searchTerm):
    rawQuery = ["SELECT * FROM craigslist_forsale_us WHERE postTitle LIKE \'% " , searchTerm,  
    "%\' AND price > 0 AND price <= 10000;"]
    query = "".join(rawQuery)

    with mydb.cursor() as cursor:
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())

    return(pd.DataFrame(result))



# taking inputs to make plot
def create_plot(searchTerm, citySelect):
    sns.set(style="white")

    # relevant df's
    raw = pullDat(searchTerm)
    d1 = raw[[5]]
    d2 = raw[[5]].loc[raw[3] == citySelect]

    # set up the matplotlib figure
    f, ax = plt.subplots(figsize=(5, 5))

    # plots
    sns.kdeplot(d1.squeeze(), label="US", color='darkblue', 
        fill=True)
    sns.kdeplot(d2.squeeze(), label=citySelect, color='red',
        fill=True).set(title='Price Distribution for ' + searchTerm + '(s)')

    # cleaning
    ax.legend()
    ax.set_xlim(-50, 5000)
    ax.set(yticklabels=[])
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    
    return f


def _clear():
    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)


# produces plot
def finalPlot():
    fig = create_plot(entry.get(), combo_box.get())

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack()



# taking search bar and dropdown selection as inputs,
# sends to 'finalPlot'
def submit():
    finalPlot()

# deletes text in search bar
def clear():
    #entry.delete(0,END)
    _clear() 

# resets search bar and drop down
def clearAll():
    entry.delete(0,END) # deletes line of text
    combo_box.set('Search')
    _clear()

    # canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    # canvas.draw()
    # canvas.get_tk_widget().pack()
    #canvas.delete('all')

    #fig = create_plot(entry.get(), combo_box.get())
    #fig = create_plot(entry.delete(0,END), combo_box.set('Search'))




#if 




# --- main ---
root = tkinter.Tk()
root.title("CraigSearch")
root.geometry("1200x1200")


# search and clear buttons with placement
submit = Button(root, text="Submit", command=submit).pack(side=RIGHT)
clear = Button(root, text='Clear', command=clear).pack(side=RIGHT)
clearAll = Button(root, text='Clear All', command=clearAll).pack(side=RIGHT)

# reset button
reset = Button(root, text="Reset", command=restart_program)
reset.pack(side=RIGHT)

# search bar
sBar = Label(root, text='Enter search term')
sBar.pack(pady=20)
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