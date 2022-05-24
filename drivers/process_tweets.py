# First party imports 
from screenshot import take_screenshot
from vt import vtscan

# Third party imports

import time
import ast
import re
import pandas as pd

def extract_urls(url_data): # Function extracts URLs from URL entity in Twitter metadata
    try:
        x = ast.literal_eval(url_data)
        dict=x[0]
        expanded_url=dict['expanded_url']
        return expanded_url
    except Exception as e:
        pass

def process_tweet(filename): # Function reads each tweet id from the file and grabs screenshots
    # More functionality can be added in the future
    # Change file path as needed

    file=pd.read_csv("/home/sayaksr/Desktop/git/blockchain_codebase/output/"+str(filename)+".csv")
    for index, row in file.iterrows():
        
        # From metadata csv

        tweet_id=row['id']
        tweet_text=row['text']
        url_data=row['entities.urls']
        
        # Extracted data

        extracted_url=extract_urls(url_data)

        
        
        print("Getting screenshot for tweet id:"+str(tweet_id))
        #take_screenshot(tweet_id)
        #extract_urls(tweet_text)

process_tweet('NFT')