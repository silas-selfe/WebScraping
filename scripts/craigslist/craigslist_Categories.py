
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
import numpy as np
from datetime import datetime

import mysql.connector
import warnings



warnings.filterwarnings("ignore")





# generates URL for each city and each category
def get_url(city, abbr):
	return(f'https://{city}.craigslist.org/search/{abbr}?')


# establishes and verifies connection with URL & formats to text
def get_pages(url):
	response = get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')

	# some city pages are 'no.js' and are difficult to scrape from - this removes those
	results_num = html_soup.find('div', class_= 'search-legend')
	if results_num is None:
		return 
	elif results_num.find('span', class_='button pagenum').text == 'no results':
		return
	else:
		results_total = int(results_num.find('span', class_='totalcount').text)
		return(np.arange(0, results_total+1, 120))


# groups subcategories
# each subcategory is followed by its three letter associated URL abbreviation
def whichCategory(cat):
	if cat == 'vehicles': 
		vehicles = ['atv/utv/sno','sna', 'auto parts','pta', 'aviation','ava',
		 'boat parts','bpa', 'boats','boo', 'cars+trucks','cta', 'heavy equip','hva',
		  'motorcycles','mca', 'motorcycle parts','mpa', 'trailers','tra', 'wheels+tires','wta']
		return vehicles

	elif cat == 'outdoors': 			# outdoors
		outdoors = ['bikes','bia', 'bike parts','bip', 'farm+garden','gra', 
		'rvs+camp','rva', 'sporting','sga']
		return outdoors

	elif cat == 'home': 				# home
		home = ['antiques','ata', 'appliances','ppa', 'baby+kid','baa', 'beauty+hlth','haa', 
		'books','bka', 'cds/dvd/vhs','ema', 'clothes+acc','cla', 'collectibles','cba',
		 'furniture','fua', 'household','hsa', 'jewelry','jwa', 'tools','tla']
		return home

	elif cat == 'computer': 			# computer
		computer = ['computer parts','syp', 'computers','sya', 
		'electronics','ela', 'cell phones','moa']
		return computer

	elif cat == 'hobbies': 				# hobbies
		hobbies = ['arts+crafts','ara', 'music instr','msa', 'photo+video','pha',
		 'toys+games','taa', 'video gaming','vga']
		return hobbies




# --- main ---



# Categories
categories = ['vehicles', 'outdoors', 'home', 'computer', 'hobbies']

# cities
# to avoid throttling, going to save per row as seen below
#cities = ["allentown","altoona","annapolis","atlanta","austin"],
#cities = ["chambersburg","charlottesville","chicago","cincinnati","cnj"]
#"dallas","delaware","denver","detroit","frederick","fredericksburg"]
#cities = ["harrisburg","harrisonburg","houston"]
#cities = ["jerseyshore","lancaster","lasvegas","lexington","losangeles"]
#cities = ["martinsburg","miami","minneapolis","newjersey","newyork","norfolk"]
#cities = ["orangecounty","pennstate","philadelphia","phoenix","poconos","portland"]
#cities = ["raleigh","reading","richmond"]
#cities = ["sacramento","savannah","sandiego","seattle","sfbay","smd","southjersey"]
cities = ["washingtondc","westmd","williamsport","winchester","york"]


# final df initialization and population
USA_sale = pd.DataFrame()
for city in cities:

	print(city)
	for cat in categories:
		catRaw = whichCategory(cat)

		post_timing = []
		post_category = []
		post_subCategory = []
		post_hoods = []
		post_title_texts = []
		post_links = []
		post_prices = []
		current = []

		print(cat)

		# subcategories
		for i in range(int(len(catRaw)/2)):
			subCatName = catRaw[::2]
			subCatAbbr = catRaw[1::2]

			url = get_url(city, subCatAbbr[i])
			pages = get_pages(url)

			print(subCatAbbr[i])

			print('-')
			print(pages)
			print('-')

			if pages is None:
				continue


			for page in pages:
				sleep(randint(1,5))
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

						# category
						post_category.append(cat)

						# subcategory
						post_subCategory.append(subCatName[i])

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
							   'category': post_category,
							   'subCategory': post_subCategory,
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
USA_sale['post title'] = USA_sale['post title'].str[:80]

# price needs a lil extra love
USA_sale['price'] = pd.to_numeric(USA_sale['price']).fillna(0)

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
queryKey = 'SELECT MAX(myKey) FROM craigslist_forsale_categories'

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
#																	*
USA_sale.to_csv('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USACatSaleWs.csv', index=False)


# query to load into db
#
# need to change filename on     ********************        LOAD DATA INFILE     *******************
#
# need to change table on     **********************           INTO TABLE         *******************
#
queryUpload = """
	LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/USACatSaleWs.csv'
	INTO TABLE craigslist_forsale_categories
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