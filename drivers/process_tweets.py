# First party imports 
from screenshot import take_screenshot

import re
import pandas as pd

def extract_urls(tweet_text): # Function extracts URLs from tweet text
    ignore_list=[] # Ignore list to filter out URLs hosted on Twitter's domain (t.co, twitter.com/...) etc
    url_regex='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' 
    try:
        urls=[]
        urls.append(re.findall(url_regex,tweet_text))        
        print(urls)
    except Exception as e:
        print(e)
        pass

def process_tweet(filename): # Function reads each tweet id from the file and grabs screenshots
    # More functionality can be added in the future
    # Change file path as needed

    file=pd.read_csv("/home/sayaksr/Desktop/git/blockchain_codebase/output/"+str(filename)+".csv")
    for index, row in file.iterrows():
        tweet_id=row['id']
        tweet_text=row['text']
        print("Getting screenshot for tweet id:"+str(tweet_id))
        #take_screenshot(tweet_id)
        extract_urls(tweet_text)

process_tweet('NFT')