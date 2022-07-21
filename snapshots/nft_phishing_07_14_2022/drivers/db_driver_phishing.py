from urllib.parse import quote_plus as urlquote
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

try:

    db = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))

except Exception as e:
    logging.warning(f"DB Fatal error! Unable to connect to NFT_Scam DB instance")
    print(e)
    time.sleep(10)



global session_phish
global session_phish
session_phish = sessionmaker(db)  
session_phish = session_phish()

base = declarative_base()

#### Table format :

# Table name: phishing

# Fields:


# 0) url_id : A unique ID attached to each URL based on the epoch timestamp when it was first seen.
# 1) url (PK) = URL of the (potential) phishing page, and also acts as identifier (primary key) of a URL
# Example: URL first seen at epoch time 1111213224 has an id: 1111213224
# 2) first_seen = Date when the URL was seen by the code
# 3) initial_state = When URL was first seen, was it Active (200) or Inactive (404)
# 4) url_became_active_time = When URL first became active (200)
# 5) url_became_inactive_time = Datestamp when URL became inactive (404)
# 4) present_state = During the last iteration, was it Active (200) or Inactive (404)
# 6) last_checked  = Datestamp when the URL was last checked.
# 8) Detection dictionary = []
    #Example: [10012359:0, 123424556:1] etc.   1=Active 0=Inactive 
    # Here the epoch timestamp acts as the unique identifier (key)  
    #   As soon as it becomes inactive (present_state=inactive) the crawler stops getting VT scores 
     
# 9) screenshot_dicitionary 
    # Screenshot every 6 hrs. Same format as VT dictionary i.e. epoch_timestamp:filename where filename is the name of the file that is stored in the local drive.
    # Example 1123234: file.png
    # filename= {url_id}_{timestamp}.png

class phishing(base): 

    __tablename__ = 'phishing' 

    # url_id, url, first_seen, initial_state, present_state, url_became_active, url_became_inactive, last_checked, time_inactive, 

    
    job_id = Column(Numeric,nullable=False)
    url_id = Column(Numeric,primary_key=True,nullable=False)
    url=Column(Text,primary_key=True,nullable=False)
    first_seen= Column(TIMESTAMP,nullable=False)
    initial_state=Column(Text,nullable=False)
    present_state=Column(Text,nullable=False)
    url_became_active_time= Column(TIMESTAMP,nullable=True)
    url_became_inactive_time= Column(TIMESTAMP,nullable=True)
    last_checked= Column(TIMESTAMP,nullable=False)
    detections=Column(Text,nullable=False)
    screenshots=Column(Text,nullable=True)



def insert_phishing_into_table(i_job_id,i_url_id,i_url,i_first_seen,i_initial_state,i_present_state,i_url_became_active_time,i_url_became_inactive_time,i_last_checked,i_detections,i_screenshots):

    base.metadata.create_all(db)

    flag=1

    try:
        # Create
        
        query = phishing(job_id=i_job_id,url_id=i_url_id,url=i_url,first_seen=i_first_seen,initial_state=i_initial_state,present_state=i_present_state,url_became_active_time=i_url_became_active_time,url_became_inactive_time=i_url_became_inactive_time,last_checked=i_last_checked,detections=i_detections,screenshots=i_screenshots)
        
        logging.info(f"Entry for URL:{i_url} inserted successfully")
        print(f"Entry for URL:{i_url} inserted successfully")
        #time.sleep(5)

        # Test insertion string. Utilize only when changing structure of db
        #query = User(job_id=1111,timestamp=1234,user_id=17689,user_name="hey",is_account_promoter="NULL",profile_description="test")  
        print("Stop 1")
        session_phish.add(query)  
        try:
            ("Stop 2")
            session_phish.commit()
        except Exception as e:
            print(e)
            time.sleep(2)
            flag=0
            print("Stop 3")
            session_phish.rollback() 
    except Exception as e:
        flag=0
        print(e)
        print(f"DB JOB ID 4444: Insertion error raised for:{i_url}")
        logging.info(f"DB JOB ID 4444: Insertion error raised for:{i_url}")
    
    return flag

