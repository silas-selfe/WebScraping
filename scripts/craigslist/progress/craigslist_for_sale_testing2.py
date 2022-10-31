
from requests import get
from bs4 import BeautifulSoup


from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
import numpy as np
import pandas as pd




cities = ["allentown",
"altoona",
"annapolis",
"atlanta",
"austin",
"boston",
"chambersburg",
"charlottesville",
"chicago",
"cincinnati",
"cnj",
"dallas",
"delaware",
"denver"]#


def get_url(city):
	return(f'https://{city}.craigslist.org/search/sss?')


def get_pages(url):
	response = get(url)
	html_soup = BeautifulSoup(response.text, 'html.parser')

	results_num = html_soup.find('div', class_= 'search-legend')
	if results_num is None:
		return 
	else:
		results_total = int(results_num.find('span', class_='totalcount').text)
		return(np.arange(0, 600, 120))




for city in cities:

	url = get_url(city)
	pages = get_pages(url)


	print(city)
	print(pages)

	# for page in pages:
	# 	response = get(url
	# 					+ "s="
	# 					+ str(page)
	# 					+ "&availabilityMode=0")
