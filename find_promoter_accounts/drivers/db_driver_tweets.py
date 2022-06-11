from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE
from urllib.parse import quote_plus as urlquote

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


import logging

logging.basicConfig(filename='pa.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# db = create_engine('postgresql+psycopg2://sayaksr:HJ[bR`m49gHT~:{\
# @128.111.49.111/nft_scam')

db = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))


def init_db_session_tweets():
    global Session_tweets
    global session_tweets
    Session_tweets = sessionmaker(db)  
    session_tweets = Session_tweets()

base = declarative_base()

class Tweet(base): 

    __tablename__ = 'tweets' 

    job_id = Column(Numeric,nullable=False)
    timestamp= Column(TIMESTAMP,nullable=False)
    tweet_id = Column(Numeric, primary_key=True,nullable=False)
    user_id = Column(Numeric,nullable=False)
    user_name=Column(Text,nullable=False)    
    tweet = Column(Text,nullable=False)
    likes=Column(Numeric,nullable=False)
    retweets=Column(Numeric,nullable=False)
    reply_count=Column(Numeric,nullable=False)



def insert_data_into_table(i_job_id,i_timestamp,i_tweet_id,i_user_id,i_user_name,i_tweet,i_likes,i_retweets,i_reply_count):


    base.metadata.create_all(db)

    try:
        # Create 
        query = Tweet(job_id=i_job_id,timestamp=i_timestamp,tweet_id=i_tweet_id,user_id=i_user_id,user_name=i_user_name,tweet=i_tweet,likes=i_likes,retweets=i_retweets,reply_count=i_reply_count)  
        session_tweets.add(query)  
        try:
            session_tweets.commit()
            logging.info(f"DB USERS (JOB ID 2222) = Tweet id: {i_tweet_id} for User:{i_user_id} inserted successfully")

        except:
            session_tweets.rollback()
            logging.info(f"DB USERS (JOB ID 2222): Insertion error raised for Tweet:{i_tweet_id} from User:{i_user_id}")


    except Exception as e:
        print(e)
