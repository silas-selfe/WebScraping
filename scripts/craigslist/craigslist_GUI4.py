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



# creating table 1 & 2
def create_tables():
    global xUpperMax
    # Table Info
    rawTable = pullDatBox('summ')
    cityInfo = rawTable.loc[rawTable[0] == combo_box.get()]
    #cityInfo = cityInfo[cityInfo[1] <= np.percentile(cityInfo[1], 90)]

    # Handling 0 search results for city
    if cityInfo.size != 0:
        cityTot = cityInfo.iat[0,1]
        cityAvg = round(cityInfo.iat[0,3])

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
    tree.insert('', 'end', text='1', values=('US', sum(rawTable['count']), avgTermPrice))
    tree.insert('', 'end', text='1', values=(combo_box.get(), cityTot, cityAvg))
    tree.place(relx=0.28, rely=0.045)
    t1.place(relx=0.28, rely=0.02)

    
    # ordering for Table 2
    topRank = rawTable.sort_values('count', ascending=False)
    botRank = rawTable.sort_values('count')
    #
    topPrice = rawTable.sort_values('avgPrice', ascending=False)
    botPrice = rawTable.sort_values('avgPrice')



    # Table 2 -- Min/Max Posts
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[0,0], topRank.iat[0,1], round(topRank.iat[0,3],2), '|',
            topPrice.iat[0,0], topPrice.iat[0,1], round(topPrice.iat[0,3],2)))
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[1,0], topRank.iat[1,1], round(topRank.iat[1,3],2), '|',
            topPrice.iat[1,0], topPrice.iat[1,1], round(topPrice.iat[1,3],2)))
    tree2.insert('', 'end', text='1', 
        values=(topRank.iat[2,0], topRank.iat[2,1], round(topRank.iat[2,3],2), '|',
            topPrice.iat[2,0], topPrice.iat[2,1], round(topPrice.iat[2,3],2)))
    
    tree2.insert('', 'end', text='1', 
        values=('---', '---', '---', '---',
            '---', '---', '---'))

    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[2,0], botRank.iat[2,1], round(botRank.iat[2,3],2), '|',
            botPrice.iat[2,0], botPrice.iat[2,1], round(botPrice.iat[2,3],2)))
    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[1,0], botRank.iat[1,1], round(botRank.iat[1,3],2), '|',
            botPrice.iat[1,0], botPrice.iat[1,1], round(botPrice.iat[1,3],2)))
    tree2.insert('', 'end', text='1', 
        values=(botRank.iat[0,0], botRank.iat[0,1], round(botRank.iat[0,3],2), '|',
            botPrice.iat[0,0], botPrice.iat[0,1], round(botPrice.iat[0,3],2)))
    
    # table and label placement
    tree2.place(relx=0.55, rely=0.41)
    t2 = Label(root, text=('Three Highest and Lowest Cities for Posts/Price'))
    t2.place(relx=0.55, rely=0.385)


# taking inputs to make plot
def create_plot():
    sns.set(style="white")

    # relevant df's
    #raw = pullDatPlot(searchTerm)
    raw = pullDatBox('raw')

    # d1 = raw[[5]]
    # d2 = raw[[5]].loc[raw[3] == citySelect]
    d1 = raw[[1]]
    print(d1.head())
    d2 = raw[[1]].loc[raw[0] == citySelect]

    # set up the matplotlib figure
    f, ax = plt.subplots(1,1,figsize=(7, 7.3))

    # plots
    sns.kdeplot(d1.squeeze(), label="US", color='darkblue', 
        fill=True)
    sns.kdeplot(d2.squeeze(), label=citySelect, color='red',
        fill=True).set(title='Price Distribution for ' + searchTerm + '(s)' + ' in ' + citySelect)

    # calling table function
    create_tables()

    # cleaning plot
    ax.legend()
    ax.set_xlim(-50, xUpperMax*3)

    ax.set(yticklabels=[])
    plt.xlabel('Price')
    plt.ylabel('Frequency')

    # yeet
    return f


# pulling all price data 
def pullDatBox(type):
    global avgTermPrice

    rawQuery = ["SELECT city, price FROM craigslist_forsale_us " 
    "WHERE postTitle LIKE \'%" , searchTerm, "%\' AND price > 0;"]

    query = "".join(rawQuery)
    with mydb.cursor() as cursor:
        cursor.execute(query)
        result = pd.DataFrame(cursor.fetchall())

    # summarized data
    dfAgg = result.groupby(0)[1].agg(['count','sum']).reset_index()
    dfAgg['avgPrice'] = dfAgg['sum'] / dfAgg['count']
    avgTermPrice = round(sum(dfAgg['sum']) / sum(dfAgg['count']))

    rawTable = pd.DataFrame(dfAgg)

    # data for posts
    rawPosts = rawTable.sort_values('count', ascending=False)
    posts = rawPosts.iloc[np.r_[0:3, len(rawPosts)-3:len(rawPosts)],0]
    posts = np.append(posts, str(citySelect))
    print(posts)

    # data for prices
    rawPrice = rawTable.sort_values('avgPrice', ascending=False)
    prices = rawPrice.iloc[np.r_[0:3, len(rawPrice)-3:len(rawPrice)],0]
    prices = np.append(prices, str(citySelect))
    print(prices)

    # all data for posts/prices
    postCities = pd.DataFrame(result[result[0].isin(posts)])
    priceCities = pd.DataFrame(result[result[0].isin(prices)])


    if type == 'post':
        return postCities
    elif type == 'price':
        return priceCities
    elif type == 'summ':
        return rawTable
    elif type == 'raw':
        return result



def boxPost():
    data = pullDatBox('post')
    data = data[data[1] <= np.percentile(data[1], 80)]

    f2, ax2 = plt.subplots(1,1,figsize=(7, 3.45))

    sns.boxplot(x=data[0], y=data[1]).set(title='Top/Bottom Highest Posts')
    plt.xticks(rotation=8)
    plt.ylabel('Price')
    plt.xlabel(' ')

    return f2


def boxPrice():
    data = pullDatBox('price')
    data = data[data[1] <= np.percentile(data[1], 90)]
    #print(np.percentile(data[1], 90))

    f3, ax3 = plt.subplots(1,1,figsize=(7, 3.45))

    sns.boxplot(x=data[0], y=data[1]).set(title='Top/Bottom Highest Priced Cities')
    plt.xticks(rotation=8)
    plt.ylabel('Price')
    plt.xlabel(' ')

    return f3


# produces plot
def finalPlot():
    global searchTerm
    global citySelect
    global canvas

    searchTerm = entry.get()
    citySelect = combo_box.get()
    fig = create_plot()
    boxFigPost = boxPost()
    boxFigPrice = boxPrice()


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx = 0.01, rely=0.14)

    canvas2 = FigureCanvasTkAgg(boxFigPost, master=root)
    canvas2.get_tk_widget().place(relx = 0.5, rely=0.01)

    canvas3 = FigureCanvasTkAgg(boxFigPrice, master=root)
    canvas3.get_tk_widget().place(relx = 0.5, rely=0.6)


# clears canvas
def _clear():
    # plot
    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)

    # this took forever to figure out
    # clears the gray plot background making way for following plot 
    canvas.get_tk_widget().pack_forget()

    # table 1
    for item in tree.get_children():
        tree.delete(item)

    # table 2
    for item in tree2.get_children():
        tree2.delete(item)

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

# resets search bar and drop down
def clearAll():
    entry.delete(0,END) # deletes line of text
    combo_box.set('Search')
    _clear()







# --- main ---






root = tkinter.Tk()
root.title("CraigSearch")
root.geometry("1500x950")


# buttons and placement
submit = Button(root, text="Submit", command=submit).place(relx = 0.15, rely=0.035)
clear = Button(root, text='Clear', command=clearAll).place(relx = 0.15, rely=0.075)
#reset = Button(root, text="Reset", command=restart_program).place(relx = 0.25, rely=0.02)

# search bar
sBar = Label(root, text='Enter search term')
sBar.place(relx = 0.05, rely=0.0195)
entry = Entry()
entry.place(relx = 0.05, rely=0.04)

# drop down menu
cityDrop = Label(root, text='Select the nearest city')
cityDrop.place(relx = 0.05, rely=0.065)

# Creating CraigSearch
combo_box = ttk.Combobox(root, value=cities)
combo_box.set('Search')
combo_box.place(relx = 0.05, rely=0.085)





# creating table
style = ttk.Style()
style.theme_use('clam')

# treeview widget
# TABLE 1 -- SEARCH RESULTS
tree = ttk.Treeview(root, 
    column=("Location", "Search Matches", "Avg Price"), 
    show='headings', height=2)

tree.column("# 1", width=100, anchor=CENTER)
tree.heading("# 1", text="Location")
tree.column("# 2", width=60, anchor=CENTER)
tree.heading("# 2", text="Results")
tree.column("# 3", width=70, anchor=CENTER)
tree.heading("# 3", text="Avg Price")

t1 = Label(root, text='Search Results')


# TABLE 2 -- CITY COMPARISONS
tree2 = ttk.Treeview(root, 
    column=("Max/Min Posts (3)", "Search Matches", "Avg Price", " ",
        "Max/Min Price", "Search Matches", "Avg Price"), 
    show='headings', height=7)

tree2.column("# 1", width=120, anchor=CENTER)
tree2.heading("# 1", text="Posts")
tree2.column("# 2", width=50, anchor=CENTER)
tree2.heading("# 2", text="Posts")
tree2.column("# 3", width=60, anchor=CENTER)
tree2.heading("# 3", text="Avg Price")

tree2.column("# 4", width=80, anchor=CENTER)
tree2.heading("# 4", text=" --- ")

tree2.column("# 5", width=100, anchor=CENTER)
tree2.heading("# 5", text="Price")
tree2.column("# 6", width=50, anchor=CENTER)
tree2.heading("# 6", text="Posts")
tree2.column("# 7", width=60, anchor=CENTER)
tree2.heading("# 7", text="Avg Price")







# initializing GUI
tkinter.mainloop()




# widget placement
# https://www.pythontutorial.net/tkinter/tkinter-place/