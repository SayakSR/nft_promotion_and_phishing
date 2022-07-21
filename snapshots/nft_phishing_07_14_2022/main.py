# First party imports

from drivers.db_driver_phishing import *
from drivers.date_time_stamp import *
#from drivers.screenshot import *
from drivers.vt import *
import json
import time

# Third-party imports

import sqlalchemy as db
import os

import logging
from urllib.parse import quote_plus as urlquote

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from sqlalchemy import create_engine
import pandas as pd

# Import virustotal module

# Import activity driver

#### FUNCTION: CHECK URL ACTIVITY ##########

def url_activity(url): # Check URL activity
    url='http://'+str(url)
    import urllib.request

    try:
        req = urllib.request.Request(url)
        req = urllib.request.urlopen(req, timeout=10)
        return 200
    except Exception as e:
        return 404

#### FUNCTION: CHECK URL ACTIVITY ##########

#### FUNCTION: VirusTotal score dictionary ########

def reading_and_updating_vtotal_dict(url_id,url,current_time,vtotal_dict):
    score=vt_scan_and_get_report(url_id,url,current_time)
    vtotal_dict[str(current_time)]=score
    vtotal_json = json.dumps(vtotal_dict, indent = 4) # Converting dict to json so Postgre supports it 
    return vtotal_json


#### FUNCTION: Getting URL screenshot

def process_screenshot(url_id,url,current_time):

    #take_screenshot(url_id,url,current_time)

    screenshot=f'{url_id}_{current_time}.png'

    return screenshot

#### FUNCTION: Getting URL Screenshots

def start_iteration():

    engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))

    date_stamp=regular_datetime()

    #os.system("python3 opensquat/opensquat.py")

    with open('results.txt') as f:
        url_list_iteration = [line.rstrip() for line in f]

    #url_list_iteration=[] # All URLs from current iteration from running opensquat

    all_urls=[] # All URLs existing in database

    [url_list_iteration.append(x) for x in url_list_iteration if x not in url_list_iteration] # Remove duplicate URL entries

    try:

        sql1 = "select * from phishing"

        url_database = pd.read_sql(sql1,con=engine) # All CSVs from database
        
        for index, row in url_database.iterrows():
            url=row['url']
           
            all_urls.append(url)
            

    except Exception as e: # This means database 'phishing' has not been created yet or there is a programming error.
        
        pass       
        
    

    # Now processing each URL from the iteration

    for i in url_list_iteration:
        print("Here")

        current_time=fetch_time()

        date_stamp=regular_datetime()

        if i not in all_urls:

            # Scenario 1: The URL does not exist in the database
            url_id=fetch_time()
            url=i
            print(url)
            first_seen=date_stamp

            initial_state=url_activity(url)
            present_state=url_activity(url)

            if(initial_state==200):
                url_became_active_time=date_stamp
                screenshots=process_screenshot(url_id,url,current_time)
            else:
                url_became_active_time=None
                screenshots=None


            url_became_inactive_time=None


            last_checked=date_stamp
            
            detection_dict={} # Initializing VTotal detection dict

            detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detection_dict)

            insert_phishing_into_table(4444,url_id,url,first_seen,initial_state,present_state,url_became_active_time,url_became_inactive_time,last_checked,detections,screenshots)

        else: 
            # Scenario 2: The URL exists in the database

            entry=url_database.loc[url_database['url'] == i]

            for index,row in entry.iterrows():
                url_id=row['url_id']
                url=row['url']
                detections=row['detections']
                initial_state=row['initial_state']
                present_state=row['present_state']
                first_seen=row['first_seen']
                url_became_active_time=row['url_became_active_time']

            # Scenario 2.1: URL's present state is 200

            if present_state==200:
                present_state=url_activity(url)

                if(present_state)==200:
                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detection_dict)
                    screenshots=reading_and_updating_screenshot_dict(url_id,url,current_time)

                    query=f"""UPDATE phishing 
                    SET last_checked = {last_checked}, detections = {detections}, screenshots = {screenshots}, url_became_inactive_time = {url_became_inactive_time}
                    WHERE url_id = '{url_id}';"""  
                
                if(present_state)==404:
                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detection_dict)
                    url_became_inactive_time=date_stamp

                    query=f"""UPDATE phishing 
                    SET last_checked = {last_checked}, detections = {detections}, url_became_inactive_time = {url_became_inactive_time}
                    WHERE url_id = '{url_id}';"""  


                    # Update database

                     

                    with engine.connect() as con:

                        rs = con.execute(query)

            
            # Scenario 2.2: URL's initial state was 200 and present state is 404

            elif initial_state==200 and present_state==404:
                # Nothing to do here
                pass
            
            # Scenario 2.3: URL's initial state was 404 and present state is also 404

            elif(url_became_active_time==None): # URL has never been active, but it might become active
                epoch_first_seen=datetime_to_epoch(first_seen)
                # Logic: If URL was first seen 10 days ago, dont bother checking it again.
                if(int(current_time)-int(epoch_first_seen)>864000):
                    # Do nothing
                    pass
                else:
                    present_state=url_activity(url)
                    if present_state==200:
                        url_became_active_time=date_stamp
                        screenshot=process_screenshot(url_id,url,current_time)
                    else:
                        url_became_active_time=None # URL still inactive

                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detection_dict)

                    # Update database

                    query=f"""UPDATE phishing 
                    SET last_checked = {last_checked}, detections = {detections}, url_became_active_time = {url_became_active_time}
                    WHERE url_id = '{url_id}';"""   

                    with engine.connect() as con:

                        rs = con.execute(query)                     





start_iteration()




###############################################



#### Table format :

# Table name: phishing

# Fields:

# 1) job_id = Default job id for phishing = 4444
# 2) url_id (PK) : A unique ID attached to each URL based on the epoch timestamp when it was first seen.
# Example: URL first seen at epoch time 1111213224 has an id: 1111213224
# 3) first_seen = Date when the URL was seen by the code
# 4) initial_state = When URL was first seen, was it Active (200) or Inactive (404)
# 5) present_state = During the last iteration, was it Active (200) or Inactive (404)
# 6) url_became_active_time = Time when URL first became active
# 7) url_became_inactive_time = Time when URL became inactive 
# 8) last_checked = Datestamp when the URL was last checked.
# 9) detections =  # VirusTotal scores every hour. It is a dictionary with format {timestamp1:detection_rate1,timestamp2:detection_rate2}.... 
                    # Stops when the URL becomes inactive.
                    # Tracking detection of the websites over-time

                    # Format: 
# 10) screenshots: Screenshot filename of the active website 
                # Example: (url_id)_(current_time).png
                # The screenshot file can be found under nft_phishing/screens/





