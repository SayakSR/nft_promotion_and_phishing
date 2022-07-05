

import pandas as pd
import glob, os
import time

from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote_plus as urlquote

engine = create_engine('postgresql+psycopg2://sayaksr:%s@128.111.49.111/nft_scam'% urlquote('HJ[bR`m49gHT~:{'))

path='/home/sayaksr/git/blockchain_codebase/find_promoter_accounts/timelines'

os.chdir(path)

# ================ MAIN ======================

for filename in glob.glob("*.csv",error_bad_lines=False):

    file=pd.read_csv(f'{filename}')

    tweets=[] # Init tweets buffer
    tweet_ids=[]

    for index, row in file.iterrows():

        try:

            user_id=row['author_id']

            #print(f"Checking user id:{user_id}")
            tweet_text=row['text']
            tweets.append(tweet_text)
            user_name=row['author.username']
            tweet_id=row['id']
            tweet_ids.append(tweet_id)
            followers=row['author.public_metrics.followers_count']

            query=f"""UPDATE users_old 
                SET user_name = '{user_name}'
                WHERE user_id = {user_id};"""  

            with engine.connect() as con:

                    rs = con.execute(query)
                    print(f"Updated for:{user_name}")
            break
        except:
            pass





