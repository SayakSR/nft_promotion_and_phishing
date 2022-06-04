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
    
    file=pd.read_csv(f'{filepath}/{userid}.csv')

    for index, row in file.iterrows():

        timestamp=fetch_date()
        
        # From metadata csv
        tweet_id=row['id']

        tweet_text=row['text']
        likes=row['public_metrics.like_count']
        retweets=row['public_metrics.retweet_count']
        replies=row['public_metrics.reply_count']
        user_id=row['author_id']
        user_name=row['author.username']

        insert_data_into_table(2222,timestamp,tweet_id,user_id,user_name,tweet_text,likes,retweets,replies)
