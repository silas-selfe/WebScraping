




from bs4 import BeautifulSoup
import bs4 as bs
from selenium import webdriver
import urllib.request
#import dryscrape


#url = 'https://boston.craigslist.org/search/sss?'


# driver = webdriver.PhantomJS()
# driver.get(url)
# p_element = driver.find_element_by_class('div', class_= 'c1-search-results')
# print(p_element)


#response = get('https://altoona.craigslist.org/search/sss?')

# source = urllib.request.urlopen(url)
# soup = bs.BeautifulSoup(source, 'lxml')

# js_test = soup.find('div', class_='c1-search-results')
# print(js_test)


# session = dryscrape.Session()
# session.visit(url)
# response = session.body()
# soup = BeautifulSoup(response)
# soup.find('div', class_='c1-search-results')


#url = 'https://www.randomlists.com/random-addresses'


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options)

# driver.get('{}?qty={}'.format(url, 1346))
# html = driver.page_source
# driver.quit()

# soup = BeautifulSoup(html, 'lxml')
# result = []
# for li in soup.find('ol', class_='rand_large').find_all('li'):
# 	result.append(list(li.stripped_strings))


# print(len(result))







#url = 'https://boston.craigslist.org/search/sss#search=1~gallery~0~0'


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options)

# driver.get('{}?qty={}'.format(url, 1346))
# html = driver.page_source
# driver.quit()

# soup = BeautifulSoup(html, 'lxml')

# print(soup)
# # result = []
# for li in soup.find('ol', class_= None).find_all('li'):
# 	result.append(list(li.stripped_strings))


# print(len(result))






















# from requests import get
# from bs4 import BeautifulSoup






# #import get to call a get request on the site
from requests import get

#get the first page of the east bay housing prices
response = get('https://cincinnati.craigslist.org/search/sss') 

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')

#get the macro-container for the housing posts
posts = html_soup.find_all('li', class_= 'result-row')
print(type(posts)) #to double check that I got a ResultSet
print(len(posts)) #to double check I got 120 (elements/page)


post_one = posts[0]
print(post_one)




# #grab the price of the first post
# #post_one_price = post_one.a.text
# #post_one_price.strip()

# post_one_price = post_one.find('span', class_= 'result-price')


# #print(post_one_price)

# #grab the time and datetime it was posted
# post_one_time = post_one.find('time', class_= 'result-date')
# post_one_datetime = post_one_time['datetime']

# #print(post_one_datetime)

# #title is a and that class, link is grabbing the href attribute of that variable
# post_one_title = post_one.find('a', class_='result-title hdrlnk')
# post_one_link = post_one_title['href']

# #print(post_one_title)


# #easy to grab the post title by taking the text element of the title variable
# post_one_title_text = post_one_title.text
# #print(post_one_title_text)


# #grabs the whole segment of housing details. We will need missing value handling in the loop as this kind of detail is not common in posts
# #the text can be split, and we can use indexing to grab the elements we want. number of bedrooms is the first element.
# #sqft is the third element
# post_one_hood = post_one.find('span', class_ = 'result-hood').text.split()[0]
# post_one_hood = post_one_hood[1:-1]
# #print(post_one_hood)

# # post_one_sqft = post_one.find('span', class_ = 'housing').text.split()[2][:-3] #cleans the ft2 at the end

# # post_one_hood = posts[0].find('span', class_='result-hood').text #grabs the neighborhood, this is the problem column that requires
# # #a lot of cleaning and figuring out later.



# posts = html_soup.find_all('li', class_= 'result-row')

# print(posts)