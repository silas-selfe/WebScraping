
from requests import get
from bs4 import BeautifulSoup
import mysql.connector


from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
from datetime import datetime
import numpy as np
import pandas as pd
import warnings


warnings.filterwarnings("ignore")


# --- pulling data ---

cities = ["allentown","altoona","annapolis","atlanta","austin","boston","chambersburg","charlottesville","chicago",
"cincinnati","cnj","dallas","delaware","denver","detroit","frederick","fredericksburg","harrisburg","harrisonburg",
"houston","jerseyshore","lancaster","lasvegas","lexington","losangeles","martinsburg","miami","minneapolis","newjersey",
"newyork","norfolk","orangecounty","pennstate","philadelphia","phoenix","poconos","portland","raleigh","reading",
"richmond","sacramento","savannah","sandiego","seattle","sfbay","smd","southjersey","washingtondc","westmd",
"williamsport","winchester","york"]

#cities = ["allentown"]

# generates URL for each city
def get_url(city):
	return(f'https://{city}.craigslist.org/search/sss?')

# establishes and verifies connection with URL & formats to text
def get_pages(url):
	response = get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')

	# some city pages are 'no.js' and are difficult to scrape from - this removes those
	results_num = html_soup.find('div', class_= 'search-legend')
	if results_num is None:
		return 
	else:
		results_total = int(results_num.find('span', class_='totalcount').text)
		return(np.arange(0, results_total+1, 120))



# final df initialization and population
USA_sale = pd.DataFrame()
for city in cities:

	post_timing = []
	post_hoods = []
	post_title_texts = []
	post_links = []
	post_prices = []
	current = []

	url = get_url(city)
	pages = get_pages(url)

	if pages is None:
		continue

	print(city)
	for page in pages:
		response = get(url
						+ "s="
						+ str(page)
						+ "&availabilityMode=0")

		# defining html text
		page_html = BeautifulSoup(response.text, 'html.parser')

		# defining the posts
		posts = page_html.find_all('li', class_= 'result-row')

		# extracting data from individual posts
		for post in posts:

			if post.find('span', class_ = 'result-hood') is not None:

				# posting date 
                # grab the datetime element 0 for date and 1 for time
				post_datetime = post.find('time', class_= 'result-date')['datetime']
				post_timing.append(post_datetime)

				# neighborhoods
				post_hood = post.find('span', class_= 'result-hood').text
				post_hood = post_hood[2:-1]
				post_hoods.append(post_hood)

				# title text
				post_title = post.find('a', class_='result-title hdrlnk')
				post_title_text = post_title.text
				post_title_texts.append(post_title_text)

				# post link
				post_link = post_title['href']
				post_links.append(post_link)

				# removes the \n whitespace from each side and removes unwanted chars
				post_price = post.a.text.strip().replace("$", "").replace(",", "")
				post_prices.append(post_price)


		# df of all data for a given city
		current = pd.DataFrame({'posted': post_timing,
		               'neighborhood': post_hoods,
		               'city' : city,
		               'post title': post_title_texts,
		               'price': post_prices,
		                'URL': post_links
		               })

	# adding all cities to final df
	USA_sale = USA_sale.append(current)



# Cleaning data for SQL import
USA_sale['posted'] = pd.to_datetime(USA_sale['posted'])
USA_sale['neighborhood'] = USA_sale['neighborhood'].astype(str).str[:50]
USA_sale['city'] = USA_sale['city'].str[:50]
USA_sale['post title'] = USA_sale['post title'].str[:80]

# price needs a lil extra love
USA_sale['price'] = pd.to_numeric(USA_sale['price']).fillna(0)
USA_sale.loc[USA_sale.price > 99000, 'price'] = 0 

# dropping duplicates
USA_sale = USA_sale.drop_duplicates(subset='URL')





# --- uploading data ---



# connecting with DB
mydb = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	password = '1234',
	database = 'webscraping'
	)

cursor = mydb.cursor()


# pulling largest key from DB
#
# 		*******************			CHANGE TO CORRECT TABLE       ********************
#											*
queryKey = 'SELECT MAX(myKey) FROM craigslist_forsale_us'

with mydb.cursor() as cursor:
	cursor.execute(queryKey)
	result = cursor.fetchall()


# fitting key in accordance with DB
if result[0][0] == None:
	USA_sale.insert(loc=0, column='ID', value=range(1, len(USA_sale)+1))
else:
	maxKeyOld = result[0][0] + 1
	maxKeyNew = len(USA_sale)
	maxKeyAdj = maxKeyOld + maxKeyNew

	USA_sale.insert(loc=0, column='ID', value=range(maxKeyOld, maxKeyAdj))



# data is now ready for upload
# saving it up upload file as backup, then uploading with SQL query
#
#
#					*********************************			RENAME VERSION         ************
#																		*
USA_sale.to_csv('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USAForSale11.csv', index=False)


# query to load into db
#
# need to change filename on     ********************        LOAD DATA INFILE     *******************
#
# need to change table on     **********************           INTO TABLE         *******************
#
queryUpload = """
	LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USAForSale11.csv'
	INTO TABLE craigslist_forsale_us
	CHARACTER SET latin1
	FIELDS TERMINATED BY ','
	ENCLOSED BY '"'
	LINES TERMINATED BY '\\n'
	IGNORE 1 ROWS;
"""


# MAKE SURE TABLE IS CORRECT AND 'queryKey' MATCHES 'INTO TABLE'
#
# MAKE SURE FILE NAME MATCHES BOTH INSTANCES 
#
with mydb.cursor() as cursor:
	cursor.execute(queryUpload)

mydb.commit()


