# First party imports 
from screenshot import take_screenshot
from vtotal import *

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
        if 'twitter' in expanded_url:
            expanded_url='null' # To skip Twitter URLs
        return expanded_url
    except Exception as e:
        pass

def process_tweet(filename): # Function reads each tweet id from the file and grabs screenshots
    # More functionality can be added in the future
    # Change file path as needed
    
    dat_file=pd.read_csv("data.csv") # Initializing storage file

    file=pd.read_csv("/home/sayaksr/Desktop/git/blockchain_codebase/output/"+str(filename)+".csv")
    for index, row in file.iterrows():
        
        # From metadata csv

        tweet_id=row['id']
        tweet_text=row['text']
        url_data=row['entities.urls']
        
        # Extracted data

        extracted_url=extract_urls(url_data)
        if extracted_url=='null':
            pass
        else:
            print(extracted_url)
            #detections=vt_scan(tweet_id,extracted_url) # Invoking the VirusTotal scan module and storing detections
            #print("URL was detected by:"+str(detections))
        
        print("Getting screenshot for tweet id:"+str(tweet_id))

        new_row={'tweet_id':tweet_id, 'extracted_url':extracted_url}
        dat_file=dat_file.append(new_row,ignore_index=True)
        #take_screenshot(tweet_id)

        # Save data into a csv

        
        
        
    dat_file.to_csv("data.csv")




process_tweet('NFT')