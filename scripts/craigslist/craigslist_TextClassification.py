# https://stackabuse.com/python-for-nlp-multi-label-text-classification-with-keras/

from numpy import array
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten, LSTM
from keras.layers import GlobalMaxPooling1D
from keras.models import Model
from keras.layers.embeddings import Embedding
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.layers import Input
from keras.layers.merge import Concatenate

import pandas as pd
import numpy as np
import re

import matplotlib.pyplot as plt
import mysql.connector



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
print(df.shape)
print(df.head())

# adding categories
df['vehicles'] = 0
df['fitness'] = 0
df['home'] = 0
df['computer'] = 0
df['games'] = 0
df['outdoor'] = 0
df['everyday'] = 0
df['music'] = 0
df['kids'] = 0
df['animals'] = 0
df['uncategorized'] = 0

print(df.head())
print("vehicles:" + str(df['vehicles'][169]))


# removing any null values or empty strings
filter = df['postTitle'] != ""
df = df[filter]
df = df.dropna()

print(df['postTitle'][169])