import csv

from requests import get
from bs4 import BeautifulSoup


from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
from datetime import datetime
import numpy as np
import pandas as pd



filename = 'C:/Users/Silas/Documents/ZenithAnalytica/Industries/WebScraping/data/USAForSale4.csv'

fields = []
rows = []


with open(filename, 'r') as csvfile:
	csvreader = csv.reader(csvfile)

	fields = next(csvreader)

	for row in csvreader:
		rows.append(row)


