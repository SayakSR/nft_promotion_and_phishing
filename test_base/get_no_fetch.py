# # Utilizing Twitter API 1.1
# from sqlite3 import Timestamp
from collections import UserDict
import json
import sys
import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
# First party imports

from drivers.date_time_stamp import *
from drivers.db_driver_users import *
from drivers.db_driver_tweets import *
from drivers.get_timeline_tweets import *
from drivers.naive_heur_single import *


# Reading word list file

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

def crawl_for_users():

    logging.info("Loading previously seen user ids")
    try:
        with open('seen_user_ids.txt') as f:
            seen_ids = [line.rstrip() for line in f]
    except:
        seen_ids=[]
    
    init_db_session_tweets()
    logging.info("Creating tweets db session successful.")
    init_db_session_users()
    logging.info("Creating users db session successful.")


    print("Start crawling users")

    with open('fetch.wordlist') as f:
        wordlist = [line.rstrip() for line in f]

    timeline_path="user_timelines"
    twarc_output_path="output"

    for i in wordlist:
        datestamp=fetch_date()
        timestamp=fetch_time()
        #os.system(f'twarc2 search --start-time 2022-06-13 --archive "{i}" {twarc_output_path}/temp.jsonl')
        #os.system(f'twarc2 csv {twarc_output_path}/temp.jsonl {twarc_output_path}/temp.csv')

        temp_file=pd.read_csv(f'{twarc_output_path}/1655168093.csv')

        for index, row in temp_file.iterrows():
            #print("Reading")
            user_id=row['author_id']

        #print(f"Checking user id:{user_id}")
            tweet_text=row['text']
            tweet_id=row['id']
            user_name=row['author.username']
            followers=row['author.public_metrics.followers_count']
            userid=row['author.id']
            user_name=row['author.username'] 
            profile_description=row['author.description']
            followers_count=row['author.public_metrics.followers_count']
            retweeted=str(row['retweeted_user_id'])
            quoted=str(row['quoted_user_id'])
            #print(retweeted)
            #file=open("heyya.txt","a")
            #file.write(f"{retweeted},{tweet_id},{user_name}\n")
            #file.close()
            if containsNumber(retweeted)==False:
             

                is_promoter=check_if_tweet_is_promotion(tweet_text)
            
                if is_promoter==True:
                    #print("Hang on")
                    #time.sleep(10)
                    print(f"User {userid} is a promoter account")
                    logging.info(f"User {userid} is a promoter account")

                # Getting timelines of potential promoters
                # # For user db

                    
                    try:
                        insert_flag=insert_user_data_into_table(1111,datestamp,userid,user_name,profile_description,followers_count)
                        
                        if(insert_flag==1):
                            #print("Found")
                            #time.sleep(10)
                            print(f"User {userid} entered succesfully into dataset")
                            logging.info(f"User {userid} entered succesfully into dataset")
                            
                            os.system(f"twarc2 timeline --use-search --exclude-retweets --limit 100 {userid} {timeline_path}/{userid}.json")
                            os.system(f"twarc2 csv {timeline_path}/{userid}.json {timeline_path}/{userid}.csv")

                            file=pd.read_csv(f'{timeline_path}/{userid}.csv')

                    
                            for index, row in file.iterrows():
                                tweet_id=row['id']
                                user_id=row['author.id']
                                user_name=row['author.username']
                                tweet_text=row['text']
                                likes=row['public_metrics.like_count']
                                retweets=row['public_metrics.retweet_count']
                                replies=row['public_metrics.reply_count']
                                try:
                                    insert_data_into_table(2222,datestamp,tweet_id,user_id,user_name,tweet_text,likes,retweets,replies)
                                    print(f"Tweet id {tweet_id} for User {user_id} inserted successfully into dataset")
                                    logging.info(f"Tweet id {tweet_id} for User {user_id} inserted successfully into dataset")
                                except Exception as e:
                                    print(e)
                                    print(f"Failed to insert Tweet id {tweet_id} for User {user_id} into dataset")
                                    logging.info(f"Failed to insert Tweet id {tweet_id} for User {user_id} into dataset")
                        else:
                            pass
                            #print("Wait")
                            #time.sleep(10)
                            
                    except Exception as e:
                        print(e)
                        print(f"Failed to enter {userid} into dataset")
                        logging.warning(f"Error inserting User {userid} into dataset")
                    # For tweets db
            else:
                pass
        #os.system(f"mv {twarc_output_path}/temp.csv {twarc_output_path}/{timestamp}.csv")
        


crawl_for_users()

