from ast import BinOp
import time
import pandas as pd
from drivers.naive_heur_single import check_if_tweet_is_promotion
from drivers.date_time_stamp import *
from drivers.db_driver_promotee import *
from drivers.discord import *
import ast

import os
import json

import logging


logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# pseudo-code

# Get tweets from each account promoter every 1 hour

def process_discord_promotion(tweet_id,expanded_url,timestamp,created_at,datestamp,promoter_id):
    discord_output=discord_driver(expanded_url,timestamp)
    name=discord_output[0]
    user_id=discord_output[1]
    user_name=discord_output[2]
    bio=discord_output[3]
    follower_count=discord_output[4]


    ### ===== DATABASE PART=====

    try:
        type="Discord"
        insert_flag=insert_promotee_into_table(3333,datestamp,name,user_id,user_name,type,bio,created_at,tweet_id,promoter_id,follower_count)

        
        if(insert_flag==1):
            print(f"User {user_id} entered succesfully into dataset")
            #time.sleep(5)
            logging.info(f"User {user_id} entered succesfully into dataset")


    except Exception as e:
        print(e)
        print(f"Failed to enter {user_id} into dataset")
        logging.warning(f"Error inserting User {user_id} into dataset")




def process_promotee(tweet_id,mentions,promoter,promoter_id,created_at,datestamp): # This timestamp = Twitter converted created_at to python date time format

    # Step 1 is to extract the userid of the promoted account.
        # Step 1.1 We do this by finding the user who has been tagged in the promotion tweet (You will find this in the 'entities.mentions' column)
        word_list=['nft','metaverse'] # Words to look for in user description
        mention_data = json.loads(mentions)
        logging.info("Mention data for tweet loaded successfully")
        number_of_mentions=len(mention_data)
        k=0
        while(k<number_of_mentions): # Promotion tweet might have multiple accounts tagged

            user_id=mention_data[k]['id']
            user_name=mention_data[k]['username']
            # print(f"To be inserted {user_name}")
            # time.sleep(2)
            name=mention_data[k]['name']
            user_description=mention_data[k]['description']
            follower_count=mention_data[k]["public_metrics"]['followers_count']
            user_description_processed=user_description.lower()
            
            user_url=mention_data[k]['url']
            bio=f"{user_description},{user_url}"

            # Remove check if promotee description is NFT for now 

            # for i in word_list: 
            #     if i in user_description_processed:
                    
                    ### ===== DATABASE PART=====

            try:
                type="Twitter"
                insert_flag=insert_promotee_into_table(3333,datestamp,name,user_id,user_name,type,bio,created_at,tweet_id,promoter_id,follower_count)

                
                if(insert_flag==1):
                    print(f"User {user_id} entered succesfully into dataset")
                    #time.sleep(5)
                    logging.info(f"User {user_id} entered succesfully into dataset")


            except Exception as e:
                print(e)
                print(f"Failed to enter {user_id} into dataset")
                logging.warning(f"Error inserting User {user_id} into dataset")

    


            print("<<<<<<<<<<<< Found an NFT account! >>>>>>>>>>>>>.")
            #time.sleep(2)
            print(user_description)
            file=open("promotees.txt","a")
            file.write(f"{name},{user_id},{user_name},{bio},{datestamp},{promoter_id},null,null,null,null\n")
            file.close()
            k=k+1
        


                        
# This is the main function

# check_description(user_id)


def get_tweets_for_every_promoter(promoter_list):
    
    for promoter in promoter_list:
        try:
            timestamp=fetch_time()
        # Step 1: This function loops through the promoter_list and queries timeline of each account account and checks for new tweets every 1 hour.
            logging.info(f"Getting timelin for {promoter} at time {timestamp}")
            print(f"Getting timeline for {promoter} at time {timestamp}")
            # Top 20 tweets only
            os.system(f"twarc2 timeline --limit 20 {promoter} promoter_timelines/{promoter}_{timestamp}.json")
            logging.info(f"Fetched timeline for {promoter} at time {timestamp}")
            print(f"Fetched timeline for {promoter} at time {timestamp}")
            os.system(f"twarc2 csv promoter_timelines/{promoter}_{timestamp}.json promoter_timelines/{promoter}_{timestamp}.csv")
            tweets=pd.read_csv(f"promoter_timelines/{promoter}_{timestamp}.csv")
            
            # Step 2: Checking each tweet in a promoters timeline to see if it matches the account promoting heuristic  
            for index, row in tweets.iterrows():
                datestamp=regular_datetime() # Used to find when the promotee account (Promotee database "timestamp" column)
                print(datestamp)
                time.sleep(10)
                tweet_id=row['id']
                promoter_id=row['author_id']
                tweet_text=row['text']
                mentions=row['entities.mentions'] # Row contains users tagged by the promotion tweet

                created_at_raw=row['created_at']

                url=row['entities.urls']

                try:
                    url_json=ast.literal_eval(url) # Converts raw string into dictionary

                    expanded_url=(url_json[0]['expanded_url'])
                except:
                    pass
                
                created_at=convert_created_at(created_at_raw) # Converting Twitter created at to Python datetime stamp

                check_tweet_promotion=check_if_tweet_is_promotion(tweet_text)
                print(f"Result============{check_tweet_promotion}")

                if(check_tweet_promotion)==True:
                    
                    created_at_epoch=convert_to_epoch(created_at_raw)
                    #print(created_at_epoch)
                    current_time=fetch_time()
                    #print(current_time)
                    if int(current_time)-int(created_at_epoch)<18000:
                        # Why this condition? If the tweet is greater than 5 hours old when it is seen by the crawler, then its an old tweet and checking increase of follower count over 3 days will not be consistent.
                        # For example a tweet that was posted yesterday has its 24 hours is today. If this condition does not exists, then the crawler thinks its 24 hours is tomorrow.
                        # Thus we need to navigate these situations using this loop.

                        # Checks if a discord link is involved

                        if "discord" in expanded_url:
                            print("Discord promotion link found")
                            logging.info("Discord promotion link found")
                            process_discord_promotion(tweet_id,expanded_url,created_at_epoch,created_at,datestamp,promoter_id)
                        
                        print("Account promotion tweet!")
                        print(tweet_text)
                        # Step 3: Check if promoted account is an NFT and if so store in database 
                        process_promotee(tweet_id,mentions,promoter,promoter_id,created_at,datestamp)
        except Exception as e:
            print(e)



def run_promotee_tracker_main():
    df_promoters=pd.read_csv("account_promoters.csv",encoding='ISO-8859-1')
    promoter_list = df_promoters['user_name'].tolist()
    logging.info("Read promoter list from accounts_promoter csv")
    get_tweets_for_every_promoter(promoter_list)


