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



global Session_promo
global session_promo
Session_promo = sessionmaker(db)  
session_promo = Session_promo()

base = declarative_base()

class Promotee(base): 

    __tablename__ = 'promotee' 

    #global job_id,timestamp,user_id,user_name,is_account_promoter,profile_description,followers
    job_id = Column(Numeric,nullable=False)
    timestamp= Column(TIMESTAMP,nullable=False)
    name=Column(Text,nullable=False)
    user_id = Column(Numeric, primary_key=True,nullable=False)
    user_name=Column(Text,nullable=False)
    type=Column(Text,nullable=False)
    bio = Column(Text,nullable=True)
    tweet_created_at=Column(TIMESTAMP,primary_key=True,nullable=False)
    post_id=Column(Numeric, primary_key=True,nullable=False)
    promoted_by=Column(Numeric, primary_key=True,nullable=False)
    follower_count_at_0h=Column(Numeric,nullable=True)
    follower_count_at_8h=Column(Numeric,nullable=True)
    follower_count_at_16h=Column(Numeric,nullable=True)
    follower_count_at_24h=Column(Numeric,nullable=True)
    follower_count_at_32h=Column(Numeric,nullable=True)
    follower_count_at_40h=Column(Numeric,nullable=True)
    follower_count_at_48h=Column(Numeric,nullable=True)



    follower_count_at_72h=Column(Numeric,nullable=True)
    completed=Column(Numeric,nullable=False)



def insert_promotee_into_table(i_job_id,i_timestamp,i_name,i_user_id,i_user_name,i_type,i_bio,i_tweet_created_at,i_tweet_id,i_promoted_by,i_follow0):

    base.metadata.create_all(db)

    flag=1

    try:
        # Create
        print(i_user_id)
        query = Promotee(job_id=i_job_id,timestamp=i_timestamp,name=i_name,user_id=i_user_id,user_name=i_user_name,type=i_type,bio=i_bio,tweet_created_at=i_tweet_created_at,tweet_id=i_tweet_id,promoted_by=i_promoted_by,follower_count_at_0h=i_follow0,follower_count_at_8h=None,follower_count_at_16h=None,follower_count_at_24h=None,follower_count_at_32h=None,follower_count_at_40h=None,follower_count_at_48h=None,completed=0)  

        logging.info(f"Entry for User:{i_user_id} inserted successfully")
        print(f"Entry for User:{i_user_id} inserted successfully")
        #time.sleep(5)

        # Test insertion string. Utilize only when changing structure of db
        #query = User(job_id=1111,timestamp=1234,user_id=17689,user_name="hey",is_account_promoter="NULL",profile_description="test")  
        print("Stop 1")
        session_promo.add(query)  
        try:
            ("Stop 2")
            session_promo.commit()
        except Exception as e:
            print(e)
            time.sleep(2)
            flag=0
            print("Stop 3")
            session_promo.rollback() 
    except Exception as e:
        flag=0
        print(e)
        print(f"DB JOB ID 3333: Insertion error raised for:{i_user_id}")
        logging.info(f"DB JOB ID 3333: Insertion error raised for:{i_user_id}")
    
    return flag

