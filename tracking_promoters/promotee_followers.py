# Get follower list of each promotee account 
# This runs every hour

from drivers.date_time_stamp import *

import sqlalchemy as db
import os

import logging
from urllib.parse import quote_plus as urlquote

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from sqlalchemy import create_engine
import pandas as pd

def run_promotee_followers_main():
    engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))
    sql1 = "select * from promotee"

    promotees = pd.read_sql(sql1,con=engine)

    for index, row in promotees.iterrows():
        timestamp=fetch_time()
        promotee_user_name=row['user_name']
        #DEBUG

        logging.info(f"Checking {promotee_user_name}...")
        print(f"Checking {promotee_user_name}...")
        promotee_time=row['tweet_created_at'] # When the tweet was created/posted
        promotee_time=datetime_to_epoch(promotee_time) # Convert created at from python date time format to epoch format
        completed=row['completed']
        # 86,400 = 24 hrs
        # 172,800 = 48 hrs
        # 259,200 = 72 hrs
        if int(timestamp)-int(promotee_time)>86400 and int(timestamp)-int(promotee_time)<172800:

        # TEST
        #if int(timestamp)-int(promotee_time)>600 and int(timestamp)-int(promotee_time)<1200:  
        # TEST  
            
            # DEBUG

            logging.info(f"promotee:{promotee_user_name} has reached 24 hour mark")
            print(f"promotee:{promotee_user_name} has reached 24 hour mark")

            #DEBUG
            
            os.system(f"twarc2 timeline --limit 2 {promotee_user_name} promotee_data/{promotee_user_name}_{timestamp}.json")
            os.system(f"twarc2 csv promotee_data/{promotee_user_name}_{timestamp}.json promotee_data/{promotee_user_name}_{timestamp}.csv")
            
            # DEBUG

            logging.info(f"timeline collected and processed for promotee:{promotee_user_name}")
            print(f"timeline collected and processed for promotee:{promotee_user_name}")

            # DEBUG

            df=pd.read_csv(f"promotee_data/{promotee_user_name}_{timestamp}.csv")
            for index, row in df.iterrows():
                followers=row['author.public_metrics.followers_count']

            query=f"""UPDATE promotee 
            SET follower_count_at_24h = {followers}
            WHERE user_name = '{promotee_user_name}';"""   # Query to update the follower count at 24hrs

            with engine.connect() as con:

                rs = con.execute(query)
        
        elif int(timestamp)-int(promotee_time)>172800 and int(timestamp)-int(promotee_time)<259200:
        # TEST
        #elif int(timestamp)-int(promotee_time)>1200 and int(timestamp)-int(promotee_time)<1800:
        # TEST
            # DEBUG

            logging.info(f"promotee:{promotee_user_name} has reached 48 hour mark")
            print(f"promotee:{promotee_user_name} has reached 48 hour mark")

            #DEBUG


            os.system(f"twarc2 timeline --limit 2 {promotee_user_name} promotee_data/{promotee_user_name}_{timestamp}.json")
            os.system(f"twarc2 csv promotee_data/{promotee_user_name}_{timestamp}.json promotee_data/{promotee_user_name}_{timestamp}.csv")
            df=pd.read_csv(f"promotee_data/{promotee_user_name}_{timestamp}.csv")
            for index, row in df.iterrows():
                followers=row['author.public_metrics.followers_count']

            query=f"""UPDATE promotee 
            SET follower_count_at_48h = {followers}
            WHERE user_name = '{promotee_user_name}';"""   # Query to update the follower count at 48 hrs

            with engine.connect() as con:

                rs = con.execute(query)

        elif int(timestamp)-int(promotee_time)>259200:
        
        # TEST
        #elif int(timestamp)-int(promotee_time)>1800:
        # TEST
            # DEBUG

            logging.info(f"promotee:{promotee_user_name} has reached 72 hour mark")
            print(f"promotee:{promotee_user_name} has reached 72 hour mark")

            #DEBUG

            if(completed==0): # Check if promotee 72 hr check has already completed

                os.system(f"twarc2 timeline --limit 2 {promotee_user_name} promotee_data/{promotee_user_name}_{timestamp}.json")
                os.system(f"twarc2 csv promotee_data/{promotee_user_name}_{timestamp}.json promotee_data/{promotee_user_name}_{timestamp}.csv")
                df=pd.read_csv(f"promotee_data/{promotee_user_name}_{timestamp}.csv")
                for index, row in df.iterrows():
                    followers=row['author.public_metrics.followers_count']

                query=f"""UPDATE promotee 
                SET follower_count_at_72h = {followers}
                WHERE user_name = '{promotee_user_name}';"""   # Query to update the follower count at 72 hrs

                with engine.connect() as con:

                    rs = con.execute(query)

                # Also set completed to 1, so it follower check doesnt happen in future.

                query2=f"""UPDATE promotee 
                SET completed = 1
                WHERE user_name = '{promotee_user_name}';"""   # Query to update the follower count at 72 hrs

                with engine.connect() as con:

                    rs = con.execute(query2)
            
            else:
                    # DEBUG

                logging.info(f"promotee:{promotee_user_name} has already completed its 72 hours, skipping")
                print(f"promotee:{promotee_user_name} has already completed its 72 hours, skipping")

                    #DEBUG
        else:
                # DEBUG
            
            logging.info(f"promotee:{promotee_user_name} does not match time criteria or is too new, skipping")
            print(f"promotee:{promotee_user_name} does not match time criteria or is too new, skipping")

                #DEBUG





                


# import time

# # pseudo-code

# get_current_time

# # import database modules

# def choose_slots():
#     # This function queries the database and fills up slots (which users follower count needs to be queried in which hour)
#     for each_user in promotee_database:
#         if each_user not in "finished_promoters.txt": 
#             if(current_time-time_first_seen)>24 hours and <48 hours:
#                 get_follower_count()
#                 store_in_promotee_db_24hours()
#             elif(current_time-time_first_seen)>48 hours and <72 hours:
#                 store_in_promotee_db_48hours()
            
#             elif(current_time-time_first_seen)>72 hours and <80 hours:
#                 store_in_promotee_db_72hours()
#                 file=open("finished_promoters.txt","a") #Store this so the user does not get follower checked again.
#                 file.write("each_user")
#                 file.close()




# def get_followers_(screen_name,timestamp):
    
