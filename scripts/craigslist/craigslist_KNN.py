# https://iq.opengenus.org/text-classification-using-k-nearest-neighbors/

import mysql.connector
import pandas as pd
import numpy as np
import re

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

from sklearn.datasets import fetch_20newsgroups




# loading dataset 
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'webscraping'
    )

cursor = mydb.cursor()

# reading entire DB
cityQ = "SELECT * FROM craigslist_forsale_us;"
#
# populating data
with mydb.cursor() as cursor:
    cursor.execute(cityQ)
    df = pd.DataFrame(cursor.fetchall())

# renaming columns and dropping URL
df = df.rename(columns={0: 'id', 1: 'date', 2: 'neighborhood', 
	3: 'city',4: 'postTitle', 5:'price'})
df = df.iloc[:, :-1]


# defining categories
categories = ['vehicle', 'fitness', 'home', 'computer', 'game', 'outdoor',
		'everyday', 'music', 'kid', 'animal', 'uncategorized']

train_data = fetch_20newsgroups(subset='train',
	categories=categories, shuffle=True, random_state=42)








# First Feature
weather =['Sunny','Sunny','Overcast','Rainy','Rainy','Rainy','Overcast','Sunny','Sunny','Rainy','Sunny','Overcast','Overcast','Rainy']
# Second Feature
temp =['Hot','Hot','Hot','Mild','Cool','Cool','Cool','Mild','Cool','Mild','Mild','Mild','Hot','Mild']
# Label or target variable
play =['No','No','Yes','Yes','Yes','No','Yes','No','Yes','Yes','Yes','Yes','Yes','No']

from sklearn import preprocessing
le = preprocessing.LabelEncoder()

weather_encoded = le.fit_transform(weather)
print('Weather Encoded',weather_encoded)

temp_encoded = le.fit_transform(temp)
print('Temperature Encoded',temp_encoded)

label=le.fit_transform(play)
print('Label Encoded',label)