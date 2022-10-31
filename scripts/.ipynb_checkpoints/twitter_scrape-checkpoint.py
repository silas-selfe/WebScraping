
import snscrape.modules.twitter as sntwitter
import pandas as pd


query = "python"
query = "(Elon OR Musk) until:2022-04-27 since:2022-01-01"
tweets = []
limit = 5000


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
  
  #print(vars(tweet))
  #break
  if len(tweets) == limit:
    break
  else:
    tweets.append([tweet.date, tweet.user.username, tweet.content])
    
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet'])

  
  
