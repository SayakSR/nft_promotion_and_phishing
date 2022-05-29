import os
import pandas as pd
import re

def fetch_timeline_tweets(userid,filepath):
    os.system(f"twarc2 timeline --limit 100 {userid} {filepath}/{userid}.json")
    os.system(f"twarc2 csv {filepath}/{userid}.json {filepath}/{userid}.csv")

def process_timeline_tweets(userid,filepath):

    found = 0 # flag when account posts promoter text

    regexp = re.compile(r'^.*[0-9]+.*[a-zA-Z]+.*[0-9]+.*$')
    
    file=pd.read_csv(f'{filepath}/{userid}.csv')

    for index, row in file.iterrows():
        
        # From metadata csv

        tweet_text=row['text']

        if regexp.search(tweet_text):
            found=1 # flag when account posts promoter text
            break
    return found 
        