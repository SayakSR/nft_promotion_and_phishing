from sqlalchemy import create_engine
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Boolean, create_engine, TIMESTAMP, Numeric, DATE

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('postgresql+psycopg2://sayaksr:HJ[bR`m49gHT~:{\
@128.111.49.111/nft_scam')

base = declarative_base()

class User(base): 

    __tablename__ = 'users' 

    job_id = Column(Numeric,nullable=False)
    timestamp= Column(TIMESTAMP,nullable=False)
    user_id = Column(Numeric, primary_key=True,nullable=False)
    user_name=Column(Text,nullable=False)    
    is_account_promoter=Column(Boolean,nullable=True)
    profile_description = Column(Text,nullable=False)
    followers=Column(Numeric,nullable=False)
    following=Column(Numeric,nullable=False)



def insert_data_into_table(i_job_id,i_timestamp,i_user_id,i_user_name,i_profile_description):

    Session = sessionmaker(db)  
    session = Session()

    base.metadata.create_all(db)

    try:
        # Create 
        query = User(job_id=i_job_id,timestamp=i_timestamp,user_id=i_user_id,user_name=i_user_name,is_account_promoter=None,profile_description=i_profile_description)  
        #query = User(job_id=1111,timestamp=1234,user_id=17689,user_name="hey",is_account_promoter="NULL",profile_description="test")  
        session.add(query)  
        session.commit()
    except Exception as e:
        print(e)
        print("Error inserting data")
