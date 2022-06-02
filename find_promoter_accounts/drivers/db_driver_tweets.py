from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('postgresql+psycopg2://sayaksr:HJ[bR`m49gHT~:{\
@128.111.49.111/nft_scam')

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

    Session = sessionmaker(db)  
    session = Session()

    base.metadata.create_all(db)

    try:
        # Create 
        query = Tweet(job_id=i_job_id,timestamp=i_timestamp,tweet_id=i_tweet_id,user_id=i_user_id,user_name=i_user_name,tweet=i_tweet,likes=i_likes,retweets=i_retweets,reply_count=i_reply_count)  
        session.add(query)  
        session.commit()
    except Exception as e:
        print(e)
