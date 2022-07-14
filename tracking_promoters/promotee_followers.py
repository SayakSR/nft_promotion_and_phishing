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

    seen_users=[] # promotees seen in this iteration

    engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))
    sql1 = "select * from promotee"

    global session_promotee
    session_promotee = sessionmaker(engine)  
    session_promotee = session_promotee()

    promotees = pd.read_sql(sql1,con=engine)

    for index, row in promotees.iterrows():
        try:
            timestamp=fetch_time()
            timestamp=timestamp+25200 # To catch up with UTC
            query_time=timestamp-604800 # Query 7 days before.
            query_time_dt=convert_epoch_to_datetime(query_time) # Query time in a modified python date-time format to match with Twitter API format.
            print(timestamp)
            

            promotee_user_name=row['user_name']
            promotee_name=row['name'] # Doubles as invite code for discord channels 
            type=row['type'] # Twitter or Discord
            #DEBUG
            tweet_id=row['tweet_id']

            # Follower counts 

            follower_count_at_0h=row['follower_count_at_0h']
            follower_count_at_1h=row['follower_count_at_1h']
            
            follower_count_at_3h=row['follower_count_at_3h']
            follower_count_at_8h=row['follower_count_at_8h']

            
            follower_count_at_16h=row['follower_count_at_16h']
            follower_count_at_24h=row['follower_count_at_24h']

            
            follower_count_at_32h=row['follower_count_at_32h']
            follower_count_at_40h=row['follower_count_at_40h']
            

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

            if int(timestamp)-int(promotee_time)>3600 and int(timestamp)-int(promotee_time)<6600: # 1hr - 1hr 50 min

                if follower_count_at_1h==None:
                    follower_count_at_1h=0
                
                if follower_count_at_1h>0:
                    activate=0
                else:
                    scenario=7
                    activate=1
            
            if int(timestamp)-int(promotee_time)>10800 and int(timestamp)-int(promotee_time)<18000: # 3 - 5 hrs

                if follower_count_at_3h==None:
                    follower_count_at_3h=0
                
                if follower_count_at_3h>0:
                    activate=0
                else:
                    scenario=8
                    activate=1

            # 28,800 - 43,200
            if int(timestamp)-int(promotee_time)>28800 and int(timestamp)-int(promotee_time)<43200: # 8 - 12 hrs
                

                if follower_count_at_8h==None:
                    follower_count_at_8h=0
                
                if follower_count_at_8h>0:
                    activate=0
                else:
                    scenario=1
                    activate=1
            
            # 57600 # 72000
            if int(timestamp)-int(promotee_time)>57600 and int(timestamp)-int(promotee_time)<72000: # 16 - 20 hrs 


                if follower_count_at_16h==None:
                    follower_count_at_16h=0
                
                if follower_count_at_16h>0:
                    activate=0
                else:
                    scenario=2
                    activate=1
            # 86400 #100800
            if int(timestamp)-int(promotee_time)>86400 and int(timestamp)-int(promotee_time)<100800: # 24 - 28 hrs 
                
                
                if follower_count_at_24h==None:
                    follower_count_at_24h=0
                
                if follower_count_at_24h>0:
                    activate=0
                else:
                    scenario=3
                    activate=1
            
            # 115200 #129600
            if int(timestamp)-int(promotee_time)>115200 and int(timestamp)-int(promotee_time)<129600: # 32 - 36 hrs 
                
                if follower_count_at_32h==None:
                    follower_count_at_32h=0
                
                if follower_count_at_32h>0:
                    activate=0
                else:
                    scenario=4
                    activate=1

            # 144000 # 158400
            if int(timestamp)-int(promotee_time)>144000 and int(timestamp)-int(promotee_time)<158400: # 40 - 44 hrs
                
                if follower_count_at_40h==None:
                    follower_count_at_40h=0
                
                if follower_count_at_40h>0:
                    activate=0
                else:
                    scenario=5
                    activate=1

            # 172800 187200
            if int(timestamp)-int(promotee_time)>172800 and int(timestamp)-int(promotee_time)<187200: # 48 - 52 hrs
                scenario=6
                activate=1
            
            if activate==1 and int(completed)==0:
                if type=="Twitter":
                    try:

                        
                        os.system(f'twarc2 timeline --use-search --start-time "{query_time_dt}"  --limit 10 --exclude-retweets --exclude-replies {promotee_user_name} promotee_data/{promotee_user_name}_{timestamp}.json')
                        seen_users.append(promotee_user_name)
                        os.system(f"twarc2 csv promotee_data/{promotee_user_name}_{timestamp}.json promotee_data/{promotee_user_name}_{timestamp}.csv")
                        
                        # DEBUG

                        logging.info(f"timeline collected and processed for promotee:{promotee_user_name}")
                        print(f"timeline collected and processed for promotee:{promotee_user_name}")

                        # DEBUG

                        df=pd.read_csv(f"promotee_data/{promotee_user_name}_{timestamp}.csv")
                        for index, row in df.iterrows():
                            followers=row['author.public_metrics.followers_count']
                        seen_users.append(promotee_user_name)
                    except Exception as e:
                        print(e)
                        logging.info(f"{e}")

                   

                elif type=="Discord":

                    try:
                        discord_output=discord_get_data(promotee_name) # Promotee name = discord invite code
                        #seen_users.append(promotee_user_name)
                        followers=discord_output[4]
                        promotee_user_name=promotee_name
                    except Exception as e:
                        print(e)
                        logging.info(f"{e}")


                if scenario==7:
                    print(f"{promotee_user_name},{tweet_id}")
                    
                    
                    query=f"""UPDATE promotee 
                    SET follower_count_at_1h = {followers}
                    WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs
                
                if scenario==8:
                    print(f"{promotee_user_name},{tweet_id}")
                    
                    
                    query=f"""UPDATE promotee 
                    SET follower_count_at_3h = {followers}
                    WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""   # Query to update the follower count at 24hrs
                
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
                        WHERE user_name='{promotee_user_name}' and tweet_id = '{tweet_id}';"""  

            

                with engine.connect() as con:

                    rs = con.execute(query)
                    if(scenario==6):
                        rs = con.execute(query2)
        except Exception as e:
            print(e)
            logging.info(f"{e}")

        


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
    
