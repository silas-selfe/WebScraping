
from requests import get
from bs4 import BeautifulSoup






#import get to call a get request on the site
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




#grab the price of the first post
post_one_price = post_one.a.text
post_one_price.strip()

#grab the time and datetime it was posted
post_one_time = post_one.find('time', class_= 'result-date')
post_one_datetime = post_one_time['datetime']

#title is a and that class, link is grabbing the href attribute of that variable
post_one_title = post_one.find('a', class_='result-title hdrlnk')
post_one_link = post_one_title['href']


#easy to grab the post title by taking the text element of the title variable
post_one_title_text = post_one_title.text


#grabs the whole segment of housing details. We will need missing value handling in the loop as this kind of detail is not common in posts
#the text can be split, and we can use indexing to grab the elements we want. number of bedrooms is the first element.
#sqft is the third element
post_one_num_bedrooms = post_one.find('span', class_ = 'housing').text.split()[0]

post_one_sqft = post_one.find('span', class_ = 'housing').text.split()[2][:-3] #cleans the ft2 at the end

post_one_hood = posts[0].find('span', class_='result-hood').text #grabs the neighborhood, this is the problem column that requires
#a lot of cleaning and figuring out later.





