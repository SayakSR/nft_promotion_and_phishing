import os
import pandas as pd
import re

from psycopg2 import Timestamp

# First party imports

from drivers.db_driver_tweets import *
from drivers.date_time_stamp import *

def fetch_timeline_tweets(userid,filepath):
    os.system(f"twarc2 timeline --use-search --limit 100 {userid} {filepath}/{userid}.json")
    os.system(f"twarc2 csv {filepath}/{userid}.json {filepath}/{userid}.csv")

def process_timeline_tweets(userid,filepath):
    try:
        with open('seen_tweet_list.txt') as f: # Seen id list avoids storing data from user ids that have been seen before
            seen_tweet_list=[line.rstrip() for line in f]
    except:
        print("Need to initialize seen id file")
        seen_tweet_list=[]
    file=pd.read_csv(f'{filepath}/{userid}.csv')

    for index, row in file.iterrows():

         tweet_id=row['id']

         if tweet_id in seen_tweet_list:
            print("Tweet already seen before")
            pass # ID has already been crawled before

         else:

            timestamp=fetch_date()
            # From metadata csv

            tweet_text=row['text']
            likes=row['public_metrics.like_count']
            retweets=row['public_metrics.retweet_count']
            replies=row['public_metrics.reply_count']
            user_id=row['author_id']
            user_name=row['author.username']

            insert_data_into_table(2222,timestamp,tweet_id,user_id,user_name,tweet_text,likes,retweets,replies)

    with open('seen_tweet_list.txt', 'a') as f:
        for item in seen_tweet_list:
            f.write("%s\n" % item)
