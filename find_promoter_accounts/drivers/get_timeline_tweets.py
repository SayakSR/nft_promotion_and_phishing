import os
import pandas as pd
import re

import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from psycopg2 import Timestamp

# First party imports

from drivers.db_driver_tweets import *
from drivers.date_time_stamp import *

def fetch_timeline_tweets(userid,filepath):
    logging.info(f"== Starting timeline processes for {userid} ===")
    os.system(f"twarc2 timeline --use-search --limit 100 {userid} {filepath}/{userid}.json")
    os.system(f"twarc2 csv {filepath}/{userid}.json {filepath}/{userid}.csv")

def process_timeline_tweets(userid,filepath):
    try:
        with open('seen_tweet_list.txt') as f: # Seen id list avoids storing data from user ids that have been seen before
            seen_tweet_list=[line.rstrip() for line in f]
            logging.info("Initializing seen tweets file")
    except:
        logging.info("Creating seen tweets file")
        seen_tweet_list=[]

    file=pd.read_csv(f'{filepath}/{userid}.csv')
    logging.info("Read timeline for  seen tweets file")

    for index, row in file.iterrows():

         tweet_id=row['id']

         if tweet_id in seen_tweet_list:
            logging.info(f"Tweet {tweet_id} already seen before, skipping")
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
            try: 
                insert_data_into_table(2222,timestamp,tweet_id,user_id,user_name,tweet_text,likes,retweets,replies)
            except:
                logging.warning(f"DB JOB ID 2222: Error inserting entry into database - tweet:{tweet_id} for User:{user_id}")

    with open('seen_tweet_list.txt', 'a') as f:
        for item in seen_tweet_list:
            f.write("%s\n" % item)
