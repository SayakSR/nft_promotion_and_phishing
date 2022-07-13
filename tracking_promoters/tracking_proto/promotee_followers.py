# Get follower list of each promotee account 
# This runs every hour

from drivers.date_time_stamp import *
from drivers.discord import *

import sqlalchemy as db
import os
import string

import logging
from urllib.parse import quote_plus as urlquote

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def run_promotee_followers_main():
    engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))
    sql1 = "select * from promotee"

    global session_promotee
    session_promotee = sessionmaker(engine)  
    session_promotee = session_promotee()

    promotees = pd.read_sql(sql1,con=engine)

    for index, row in promotees.iterrows():
        timestamp=fetch_time()
        print(timestamp)
        timestamp=int(timestamp)+7200 # Adding 2 hrs to catch up with Central time

        promotee_user_name=row['user_name']
        promotee_name=row['name'] # Doubles as invite code for discord channels 
        type=row['type'] # Twitter or Discord
        #DEBUG
        tweet_id=row['tweet_id']

        logging.info(f"Checking {promotee_user_name}...")
        print(f"Checking {promotee_user_name}...")
        promotee_time=row['tweet_created_at'] # When the tweet was created/posted
        promotee_time=datetime_to_epoch(promotee_time) # Convert created at from python date time format to epoch format
        completed=row['completed']
        print(promotee_time)

        scenario=0
        activate=0
        print("Here")
        print(f"{timestamp}-{promotee_time} =========")
        print(int(timestamp)-int(promotee_time))
        if int(timestamp)-int(promotee_time)>28800 and int(timestamp)-int(promotee_time)<43200: # 8 - 12 hrs
            scenario=1
            activate=1
        
        # 57600 # 72000
        if int(timestamp)-int(promotee_time)>57600 and int(timestamp)-int(promotee_time)<72000: # 16 - 20 hrs 
            scenario=2
            activate=1
        # 86400 #100800
        if int(timestamp)-int(promotee_time)>1800 and int(timestamp)-int(promotee_time)<1800: # 24 - 28 hrs 
            scenario=3
            activate=1
        if int(timestamp)-int(promotee_time)>115200 and int(timestamp)-int(promotee_time)<129600: # 32 - 36 hrs 
            scenario=4
            activate=1

        
        if int(timestamp)-int(promotee_time)>144000 and int(timestamp)-int(promotee_time)<158400: # 40 - 44 hrs
            scenario=5
            activate=1

        if int(timestamp)-int(promotee_time)>172800 and int(timestamp)-int(promotee_time)<187200: # 48 - 52 hrs
            scenario=6
            activate=1
        
        if activate==1 and int(completed)==0:
            if type=="Twitter":

                try:
                    
                    os.system(f"twarc2 timeline --limit 2 {promotee_user_name} promotee_data/{promotee_user_name}_{timestamp}.json")
                    os.system(f"twarc2 csv promotee_data/{promotee_user_name}_{timestamp}.json promotee_data/{promotee_user_name}_{timestamp}.csv")
                    
                    # DEBUG

                    logging.info(f"timeline collected and processed for promotee:{promotee_user_name}")
                    print(f"timeline collected and processed for promotee:{promotee_user_name}")

                    # DEBUG

                    df=pd.read_csv(f"promotee_data/{promotee_user_name}_{timestamp}.csv")
                    for index, row in df.iterrows():
                        followers=row['author.public_metrics.followers_count']
                except Exception as e:
                    print(e)
            elif type=="Discord":

                try:
                    discord_output=discord_get_data(promotee_name) # Promotee name = discord invite code

                    followers=discord_output[4]
                    promotee_user_name=promotee_name
                except Exception as e:
                    print(e)
            if scenario==1:
                print(f"{promotee_user_name},{tweet_id}")
                
                
                query=f"""UPDATE promotee 
                SET follower_count_at_8h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs
            
            elif scenario==2:

                query=f"""UPDATE promotee 
                SET follower_count_at_16h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs

            elif scenario==3:

                query=f"""UPDATE promotee 
                SET follower_count_at_24h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs

            elif scenario==4:

                query=f"""UPDATE promotee 
                SET follower_count_at_32h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs

            elif scenario==5:

                query=f"""UPDATE promotee 
                SET follower_count_at_40h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs

            elif scenario==6:

                query=f"""UPDATE promotee 
                SET follower_count_at_48h = {followers}
                WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs


                query2=f"""UPDATE promotee 
                    SET completed = 1
                    WHERE user_name={promotee_user_name} and tweet_id = '{tweet_id}';"""  

        

            with engine.connect() as con:

                rs = con.execute(query)
                if(scenario==6):
                     rs = con.execute(query2)

        


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
    
