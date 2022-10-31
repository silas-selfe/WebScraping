
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



#import get to call a get request on the site







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
"denver",
"detroit",
"frederick",
"fredericksburg",
"harrisburg",
"harrisonburg",
"houston",
"jerseyshore",
"lancaster",
"lasvegas",
"losangeles",
"martinsburg",
"miami",
"minneapolis",
"newjersey",
"newyork",
"norfolk",
"orangecounty",
"pennstate",
"philadelphia",
"phoenix",
"poconos",
"portland",
"raleigh",
"reading",
"richmond",
"sacramento",
"sandiego",
"seattle",
"sfbay",
"smd",
"southjersey",
"washingtondc",
"westmd",
"williamsport",
"winchester",
"york"]



#first = f'https://{cities[0]}.craigslist.org/search/sss'

#get the first page of the east bay housing prices

#get the macro-container for the housing posts
#posts = html_soup.find_all('li', class_= 'result-row')



# cities = ["allentown",
# "altoona"]#

#first = cities[0]
#cities = cities[1:]

#url = f'https://{first}.craigslist.org/search/sss?'
# url = f'https://{cities[0]}.craigslist.org/search/sss?'

# response = get(url) 
# html_soup = BeautifulSoup(response.text, 'html.parser')

# results_num = html_soup.find('div', class_= 'search-legend')
# results_total = int(results_num.find('span', class_='totalcount').text)

# pages = np.arange(0, results_total+1, 120)







USA_sale = pd.DataFrame()
for city in cities:
#
    url = f'https://{city}.craigslist.org/search/sss?'

    response = get(url) 
    html_soup = BeautifulSoup(response.text, 'html.parser')

    results_num = html_soup.find('div', class_= 'search-legend')
    results_total = int(results_num.find('span', class_='totalcount').text)

    pages = np.arange(0, results_total+1, 120)
#


    print(city)

    iterations = 0

    post_timing = []
    post_hoods = []
    post_title_texts = []
    post_links = []
    post_prices = []
    current = []
    #USA_sale = []

    for page in pages:
        
        #get request
        response = get(url 
                       + "s=" #the parameter for defining the page number 
                       + str(page) #the page number in the pages array from earlier
                       + "&availabilityMode=0")

        sleep(randint(1,5))


        #throw warning for status codes that are not 200
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
            
        #define the html text
        page_html = BeautifulSoup(response.text, 'html.parser')

        #define the posts
        posts = page_html.find_all('li', class_= 'result-row')

        #extract data item-wise
        for post in posts:

            if post.find('span', class_ = 'result-hood') is not None:

                #posting date
                #grab the datetime element 0 for date and 1 for time
                post_datetime = post.find('time', class_= 'result-date')['datetime']
                post_timing.append(post_datetime)

                #neighborhoods
                post_hood = post.find('span', class_= 'result-hood').text
                post_hood = post_hood[2:-1]
                post_hoods.append(post_hood)

                #title text
                post_title = post.find('a', class_='result-title hdrlnk')
                post_title_text = post_title.text
                post_title_texts.append(post_title_text)

                #post link
                post_link = post_title['href']
                post_links.append(post_link)
                
                #removes the \n whitespace from each side, removes the currency symbol, and turns it into an int
                post_price = post.a.text.strip().replace("$", "").replace(",", "")
                post_prices.append(post_price)




        current = pd.DataFrame({'posted': post_timing,
                           'neighborhood': post_hoods,
                           'city' : city,
                           'post title': post_title_texts,
                           'price': post_prices,
                            'URL': post_links
                           })
        #USA_sale.append(current)
    #print(current)
    #USA_sale.concat(current)

    USA_sale = USA_sale.append(current)




#first things first, drop duplicate URLs because people are spammy on Craigslist. 
#Let's see how many uniqe posts we really have.

#USA_sale = USA_sale.drop_duplicates(subset='URL')
#len(USA_sale.drop_duplicates(subset='URL'))



# #convert datetime string into datetime object to be able to work with it
# from datetime import datetime

# eb_apts['posted'] = pd.to_datetime(eb_apts['posted'])


#USA_sale = pd.DataFrame(USA_sale)
#USA_sale['price'] = USA_sale['price'].fillna(0)
USA_sale.to_csv('C:/Users/Silas/Documents/ZenithAnalytica/Industries/WebScraping/data/USAForSale2.csv')



# Misc

#print(type(posts)) #to double check that I got a ResultSet
#print(len(posts)) #to double check I got 120 (elements/page)

# post_one = posts[0]


# #grab the price of the first post
# #post_one_price = post_one.a.text
# #post_one_price.strip()
# post_one_price = post_one.find('span', class_= 'result-price')


# #grab the time and datetime it was posted
# post_one_time = post_one.find('time', class_= 'result-date')
# post_one_datetime = post_one_time['datetime']


# #title is a and that class, link is grabbing the href attribute of that variable
# post_one_title = post_one.find('a', class_='result-title hdrlnk')
# post_one_link = post_one_title['href']


# #easy to grab the post title by taking the text element of the title variable
# post_one_title_text = post_one_title.text
# #print(post_one_title_text)


# #grabs the whole segment of housing details. We will need missing value handling in the loop as this kind of detail is not common in posts
# #the text can be split, and we can use indexing to grab the elements we want. number of bedrooms is the first element.
# #sqft is the third element
# post_one_hood = post_one.find('span', class_ = 'result-hood').text.split()[0]
# post_one_hood = post_one_hood[1:-1]
#print(post_one_hood)

# post_one_sqft = post_one.find('span', class_ = 'housing').text.split()[2][:-3] #cleans the ft2 at the end

# post_one_hood = posts[0].find('span', class_='result-hood').text #grabs the neighborhood, this is the problem column that requires
# #a lot of cleaning and figuring out later.







#build out the loop


