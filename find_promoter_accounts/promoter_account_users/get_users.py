# Utilizing Twitter API 1.1
from sqlite3 import Timestamp
import tweepy
import json

# First party imports

from drivers.date_time_stamp import *
from drivers.db_driver import *

# Credentials

consumer_key= 'tkta9r8G5FD77q4vZtLwNwOpK'
consumer_secret = 'EJaEnpD1YYF1kNodh94tnJw3Uyv2K625KFepGVwx3Pi38bNVM3'
access_token ='1354188624854659072-5Zje7xDG6IX4MT91u9KR8z8D9QiH7m'
access_token_secret='MT50ifwvCEiP9PMksPyUeT4goV4nLDsg0cAqItfO1aLHw'

  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
auth.set_access_token(access_token, access_token_secret)
  
api = tweepy.API(auth, wait_on_rate_limit= True)
  
q = "dm for promotions"
file_path="user_metadata/"
page_num=0 # Init page number variable, max pages = 50

while page_num<=2:

    page_num=page_num+1
# search the query
    users = api.search_users(q,page=page_num)

    # print the users retrieved
    for user in users:

        timestamp=fetch_date() # To be stored in database 

        user_id=str(user.id_str)
        user_name=str(user.name)
        profile_description=str(user.description)
        file=open(f'{file_path}{user_id}.json','w',encoding='utf-8')
        user_json_str = json.dumps(user._json)
        file.write(user_json_str)
        file.close()

        insert_data_into_table(1111,timestamp,user_id,user_name,profile_description)

    
