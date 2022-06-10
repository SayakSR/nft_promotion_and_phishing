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


def init_db_session_users():
    global Session_users
    global session_users
    Session_users = sessionmaker(db)  
    session_users = Session_users()

base = declarative_base()

class User(base): 

    __tablename__ = 'users' 

    #global job_id,timestamp,user_id,user_name,is_account_promoter,profile_description,followers
    job_id = Column(Numeric,nullable=False)
    timestamp= Column(TIMESTAMP,nullable=False)
    user_id = Column(Numeric, primary_key=True,nullable=False)
    user_name=Column(Text,nullable=False)
    is_account_promoter=Column(Boolean,nullable=True)
    profile_description = Column(Text,nullable=False)
    followers=Column(Numeric,nullable=False)
    #following=Column(Numeric,nullable=False)



def insert_user_data_into_table(i_job_id,i_timestamp,user_id,i_user_name,i_profile_description,i_followers):

    base.metadata.create_all(db)

    try:
        # Create
        print(user_id)
        query = User(job_id=i_job_id,timestamp=i_timestamp,user_id=user_id,user_name=i_user_name,is_account_promoter=None,profile_description=i_profile_description,followers=i_followers)  
        logging.info(f"Entry for User:{user_id} inserted successfully")

        # Test insertion string. Utilize only when changing structure of db
        #query = User(job_id=1111,timestamp=1234,user_id=17689,user_name="hey",is_account_promoter="NULL",profile_description="test")  
        session_users.add(query)  
        session_users.commit()
    except Exception as e:
        print(e)
        logging.info(f"DB JOB ID 1111: Insertion error raised for:{user_id}")

