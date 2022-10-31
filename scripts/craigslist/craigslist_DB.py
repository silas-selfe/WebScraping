# Inserting Records in Tables - for later
# https://realpython.com/python-mysql/

import mysql.connector
import json
import math
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np



mydb = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	password = '1234',
	database = 'webscraping'
	)

cursor = mydb.cursor()

#pulling largest key from DB
query = 'SELECT MAX(myKey) FROM craigslist_forsale_us'

with mydb.cursor() as cursor:
	cursor.execute(query)
	result = cursor.fetchall()
	#result = result[0]
	#result = pd.DataFrame(cursor.fetchall())

print(result[0][0])
# maxKeyOld = result[0] + 1
# print(maxKeyOld)
# maxKeyNew = 49 #len(newdf)
# maxKeyAdj = maxKeyOld + maxKeyNew







# query = 'SELECT * FROM craigslist_forsale_us WHERE myKey < 50'

# with mydb.cursor() as cursor:
# 	cursor.execute(query)
# 	#result = cursor.fetchall()
# 	#result = result[0]
# 	result = pd.DataFrame(cursor.fetchall())


#maxKeyOld = result[0] + 1
#print(maxKeyOld)




#df = pd.DataFrame(result)
# df[0] = range(maxKeyOld, maxKeyAdj)

#print(query)
#df = df.iloc[: , 1:]
#df.insert(loc=0, column='ID', value=range(maxKeyOld, maxKeyAdj))





# print(len(df))
#print(df.head())


























