# First party imports

from drivers.db_driver_phishing import *
from drivers.date_time_stamp import *
from drivers.screenshot import *
from drivers.vt import *
import json
import time

from urllib.parse import quote_plus as urlquote
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from drivers.activity import url_activity

import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Third-party imports

import sqlalchemy as db
import os
import random

import logging
from urllib.parse import quote_plus as urlquote

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from sqlalchemy import create_engine
import pandas as pd
import time


# Import virustotal module

# Import activity driver


def save_webpage(url_id,url,current_time):
    os.system(f"wget -p -k {url} >/dev/null 2>&1")
    try:
        url=url[7:]
        os.system(f"cp -r {url} saved_webpages/{url_id}_{current_time}")
        os.system (f"rm -r {url}")
        filename=f"{url_id}_{current_time}"
        return filename
    except Exception as e:
        print(e)


#### FUNCTION: CHECK URL ACTIVITY ########## {Depreciated driver, new driver in /drivers/activity.py }

# def url_activity(url): # Check URL activity
#     url='http://'+str(url)
#     import urllib.request

#     try:
#         req = urllib.request.Request(url)
#         req = urllib.request.urlopen(req, timeout=10)
#         return 200
#     except Exception as e:
#         print(e)
#         return 404

#### FUNCTION: CHECK URL ACTIVITY ##########

#### FUNCTION: VirusTotal score dictionary ########

def reading_and_updating_vtotal_dict(url_id,url,current_time,vtotal_dict):
    score=vt_scan_and_get_report(url_id,url,current_time)
    vtotal_dict[str(current_time)]=score
    vtotal_json = json.dumps(vtotal_dict, indent = 4) # Converting dict to json so Postgre supports it 
    return vtotal_json


#### FUNCTION: Getting URL screenshot

def process_screenshot(url_id,url,current_time,last_screenshoted):

     # This function also deals with saving full webpage snapshots 

    if last_screenshoted==None:
        last_screenshoted=0
        file_name=take_screenshot(url_id,url,current_time)
        save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage


    elif last_screenshoted==0:
        
        file_name=take_screenshot(url_id,url,current_time)
        save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage

    
    else:
        last_screenshoted_epoch=datetime_to_epoch(last_screenshoted)

        if(int(current_time)-int(last_screenshoted_epoch)) > 14400: # Take screenshots every four hours.
  
            file_name=take_screenshot(url_id,url,current_time)
            save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage


        else:
            print("URL is not 4hrs old yet")
            file_name="pass"

    return file_name

# Function to take screenshot snapshot

def process_save_webpage(url_id,url,current_time,last_screenshoted):

    if last_screenshoted==None:
        last_screenshoted=0
        save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage
        return save_file


    elif last_screenshoted==0:
        
        save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage
        return save_file
    
    else:
        last_screenshoted_epoch=datetime_to_epoch(last_screenshoted)

        if(int(current_time)-int(last_screenshoted_epoch)) > 14400: # Take screenshots every four hours.
  
            save_file=save_webpage(url_id,url,current_time) # Take a full snapshot of the webpage
            return save_file

        else:
            print("URL is not 4hrs old yet")
            file_name="pass"

    

     

#### FUNCTION: Getting URL Screenshots

    
        
def start_iteration():



    engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))


    global session_phish
    global session_phish
    session_phish = sessionmaker(engine)  
    session_phish = session_phish()

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
        
        print(e)       
        
    

    # Now processing each URL from the iteration

    for i in url_list_iteration:
        print("Here")

        current_time=fetch_time()

        date_stamp=regular_datetime()

        url=i
        raw_url=i # Raw URL without the http
        if 'http://' not in url or 'https://' not in url:
            url='http://'+url
            print(url)

        if url not in all_urls:

            # Scenario 1: The URL does not exist in the database
            print("Scenario 1 invoked")
            url_id=fetch_time()
            offset = random.randint(1000,9999)
            url_id=int(url_id)+int(offset)
            
            first_seen=date_stamp

            initial_state=url_activity(url)
            present_state=url_activity(url)

            last_checked=date_stamp

            if(initial_state==200):
                url_became_active_time=date_stamp
                last_screenshoted=None
                screenshots=process_screenshot(url_id,url,current_time,last_screenshoted)
                webpage_filename=process_save_webpage(url_id,url,current_time,last_screenshoted)
                
                last_screenshoted=last_checked

            else:
                url_became_active_time=None
                screenshots=None
                last_screenshoted=None
                webpage_filename=None




            url_became_inactive_time=None


            

            
            detections={} # Initializing VTotal detection dict

            detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detections)

            insert_phishing_into_table(4444,url_id,url,first_seen,initial_state,present_state,url_became_active_time,url_became_inactive_time,last_checked,detections,screenshots,last_screenshoted,webpage_filename)

        else: 
            # Scenario 2: The URL exists in the database
            print("Scenario 2 invoked")
            entry=url_database.loc[url_database['url'] == url]
            print(entry)

            for index,row in entry.iterrows():

                url_id=row['url_id']
                url=row['url']
                detections=row['detections']
                detections = json.loads(detections)
                print(detections)
                initial_state=row['initial_state']
                present_state=row['present_state']
                print(present_state)
                last_screenshoted=row['last_screenshoted']
                first_seen=row['first_seen']
                first_seen_epoch=datetime_to_epoch(first_seen)
                url_became_active_time=row['url_became_active_time']

            # Scenario 2.1: URL's present state is 200
            if int(present_state)==200:
                print("Scenario 2.1 invoked")

                present_state=url_activity(url)

                if int(present_state)==200:
                    if(last_screenshoted)==None:
                        last_screenshoted=0
                        
                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detections)
                    screenshots=process_screenshot(url_id,url,current_time,last_screenshoted)
                    webpage_filename=process_save_webpage(url_id,url,current_time,last_screenshoted)


                    # query=f"""UPDATE phishing 
                    # SET last_checked = {last_checked}, detections = {detections}, screenshots = {screenshots}, url_became_inactive_time = {url_became_inactive_time}
                    # WHERE url_id = '{url_id}';"""  

                    q211 = session_phish.query(phishing).filter(phishing.url_id == url_id).one()
                    q211.last_checked = last_checked
                    q211.last_screenshoted=last_checked
                    q211.detections=detections
                    if screenshots=="pass":
                        pass
                    else:
                        q211.screenshots=screenshots
                        q211.webpage_filename=webpage_filename
                        
                    q211.url_became_active_time=url_became_active_time

                    session_phish.commit()
                
                if int(present_state)==404:
                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detections)
                    url_became_inactive_time=date_stamp

                    # query=f"""UPDATE phishing 
                    # SET last_checked = {last_checked}, detections = {detections}, url_became_inactive_time = {url_became_inactive_time}
                    # WHERE url_id = '{url_id}';""" 

                    q212 = session_phish.query(phishing).filter(phishing.url_id == url_id).one()
                    q212.last_checked = last_checked
                    q212.detections=detections
                    q212.url_became_inactive_time=url_became_inactive_time 

                    session_phish.commit()

                    # Update database

                     

                    # with engine.connect() as con:

                    #     rs = con.execute(query)

            
            # Scenario 2.2: URL's initial state was 200 and present state is 404
            
            elif int(initial_state)==200 and int(present_state)==404:
                print("Scenario 2.2 invoked")
                # Nothing to do here
                pass
            
            # Scenario 2.3: URL's initial state was 404 and present state is also 404
           
            elif int(initial_state)==404 and int(present_state)==404: # URL has never been active, but it might become active
                print("Scenario 2.3 invoked")
                epoch_first_seen=datetime_to_epoch(first_seen)
                # Logic: If URL was first seen 10 days ago, dont bother checking it again.
                if(int(current_time)-int(epoch_first_seen)>864000):
                    # Do nothing
                    pass
                else:
                    print(url)
                    #time.sleep(3)
                    present_state=url_activity(url)
                    print(f"Debug present state:{present_state}")
                    time.sleep(3)
                    if int(present_state)==200:
                        url_became_active_time=date_stamp
                        last_screenshoted=0
                        screenshots=process_screenshot(url_id,url,current_time,last_screenshoted)
                        webpage_filename=process_save_webpage(url_id,url,current_time,last_screenshoted)

                        q23.screenshots=screenshots
                        q23.webpage_filename=webpage_filename
                        q23.present_state=present_state
                        

                    else:
                        url_became_active_time=None # URL still inactive

                    last_checked=date_stamp
                    detections=reading_and_updating_vtotal_dict(url_id,url,current_time,detections)

                    # Update database

                    # query=f"""UPDATE phishing 
                    # SET last_checked = {last_checked}, detections = {detections}, url_became_active_time = {url_became_active_time}
                    # WHERE url_id = '{url_id}';"""   

                    q23 = session_phish.query(phishing).filter(phishing.url_id == url_id).one()
                    q23.last_checked = last_checked
                    q23.last_screenshoted=last_checked
                    q23.detections=detections
                    q23.url_became_active_time=url_became_active_time 

                    session_phish.commit()


                    # with engine.connect() as con:

                    #     rs = con.execute(query)                     





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

# 11) last_screenshoted : Time when last screenshot (python datetime format)





