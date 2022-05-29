# First party imports 

from drivers.timeline_processes import *

# Third party imports

import time
import ast
import re
import pandas as pd


def process_tweet(filepath): # Function reads each tweet id from the file and grabs screenshots
    # More functionality can be added in the future
    # Change file path as needed

    file=pd.read_csv(str(filepath))
    file = file.drop_duplicates(subset='author_id', keep="first")

    for index, row in file.iterrows():
        
        # From metadata csv

        author_id=row['author_id']
        author_description=row['author.description']
        author_followers_count=row['author.public_metrics.followers_count']
        author_username=row['author.username']
        author_description=str(author_description).replace(",","") # Removing commas

        # Only consider if author followercount >= 100k

        if(int(author_followers_count)>=100000):
            # Collecting timeline (100 latest tweets) for the user

            timeline_path=f'raw_output/timelines/'
            fetch_timeline_tweets(str(author_id),timeline_path)
            # Checks if timeline tweets matches promoter account regex

            check_if_promoter=process_timeline_tweets(str(author_id),timeline_path)

            if int(check_if_promoter)==1:

                file=open("promoter_accounts/accounts.csv","a",encoding="utf-8")
                file.write(f"{author_id},{author_username},{author_description},{author_followers_count}")
                file.write("\n")
                file.close()