# Utilizing Twitter API 1.1
from sqlite3 import Timestamp
import tweepy
import json

import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
# First party imports

from drivers.date_time_stamp import *
from drivers.db_driver_users import *
from drivers.get_timeline_tweets import *


# Credentials

consumer_key= 'tkta9r8G5FD77q4vZtLwNwOpK'
consumer_secret = 'EJaEnpD1YYF1kNodh94tnJw3Uyv2K625KFepGVwx3Pi38bNVM3'
access_token ='1354188624854659072-5Zje7xDG6IX4MT91u9KR8z8D9QiH7m'
access_token_secret='MT50ifwvCEiP9PMksPyUeT4goV4nLDsg0cAqItfO1aLHw'

# Reading word list file

def crawl_for_users():
    
    init_db_session_tweets()
    logging.info("Creating tweets db session successful.")
    init_db_session_users()
    logging.info("Creating users db session successful.")


    print("Start crawling users")

    with open('common.wordlist') as f:
        wordlist = [line.rstrip() for line in f]



    try: # Seen id list avoids storing data from user ids that have been seen before
        with open('seen_id_list.txt') as f:
            seen_id_list=[line.rstrip() for line in f]
    except:
        print("Need to initialize seen id file")
        logging.info("Created seen user id file")

        seen_id_list=[]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth,wait_on_rate_limit= True)

    #initial_q = "dm for promotions" # Comment out because entire query is being sourced from common.wordlist now

    file_path="user_metadata/"
    page_num=0 # Init page number variable, max pages = 50

    for i in wordlist:
        q=f" {i}" # query changes based on word list

        logging.info("get_users module sleeping for 10 secs to avoid hitting API limit error")

        time.sleep(10) # Sleeping timer to keep api limit in check
        
        # Why 10 secs? Takes about ~ 40 secs to make 50 calls (pages in each request). API limit is 900 calls/15 min
        # the loop essentially runs 18 times to reach 900 calls. 18 calls takes 720 secs approx ~ 12 mins. 
        # Putting a sleep time of 10 secs between each call for 18 calls buys us that 3 mins of extra time.
          
        
        print(f"Looking for user accounts using query:{q}")
        page_num=1 # Resetting page_num counter
        while page_num<=50:

            page_num=page_num+1
        # search the query
            logging.info(f"Query {q} is being used to search for users now")

            users = api.search_users(q,page=page_num)

            # print the users retrieved
            for user in users:

                timestamp=fetch_date() # To be stored in database 

                user_id=str(user.id_str)
                if user_id in seen_id_list:
                    logging.info(f"Skipping User:{user_id} because it has already been crawled before.")

                    pass # ID has already been crawled before
                else:
                    seen_id_list.append(user_id)
                    user_name=str(user.name)
                    profile_description=str(user.description)
                    file=open("profile_desc.txt","a",encoding='utf-8')
                    file.write(str(profile_description))
                    logging.info(f"Profile description for User:{user_id} written successfully")

                    file.close()
                    file=open(f'{file_path}{user_id}.json','w',encoding='utf-8')
                    user_json_str = json.dumps(user._json)
                    file.write(user_json_str)
                    followers_count=str(user.followers_count)
                    file.close()
                    try:
                        insert_user_data_into_table(1111,timestamp,user_id,user_name,profile_description,followers_count)
                        fetch_timeline_tweets(user_id,"timelines")
                        try:
                    	    process_timeline_tweets(user_id,"timelines") # This function will also commit to database as necessary
                        except:
                            logging.warning(f"Error processing timeline for user id {user_id}. Probable cause is file does not exist.")

                    except:
                        logging.warning(f"DB JOB ID 1111: Error inserting entry into database for User:{user_id}")

                    # ==== Collecting tweets ======

                    
            users=[] # Emptying the user buffer. Not really needed, but just being extra careful that old ids dont get fetched again
            with open('seen_id_list.txt', 'a') as f:
                for item in seen_id_list:
                    f.write("%s\n" % item)



crawl_for_users()
