

import pandas as pd
import glob, os
import time

path='/home/sayaksr/git/blockchain_codebase/find_promoter_accounts/timelines'

os.chdir(path)

def check_if_user_has_enough_followers(followers):
    threshold=100
    if int(followers)>threshold:
        return True
    else:
        return False

def check_if_tweet_is_promotion(tweet):

    # Init flags at start of every tweet
    flag_1,flag_2,flag_3,flag_4,flag_5,flag_6=0,0,0,0,0,0

    import re
    word = 'fubar'
    value_dol_regex = re.compile(r'\$[0-9]+')
    value_jt_regex=re.compile(r'JT[0-9]+')

    tweet_processed=tweet.lower()

    if "|" in tweet_processed or '~' or 'idr' in tweet_processed:
        flag_1=True

    if "nft" or "crypto" or "WL" or "whitelist" or "white-list" or "white list" not in tweet_processed:
        flag_11=True
    
    if int(len(tweet_processed))>150:
        flag_12=False
    else:
        flag_12=True

    if value_dol_regex.search(tweet_processed) or value_jt_regex.search(tweet_processed) or '~' in tweet_processed or 'idr' in tweet_processed:
        flag_2=True

    if 'rt' in tweet_processed or 'retweet' in tweet_processed:
        flag_3=True
    if 'follow' in tweet_processed:
        flag_4=True

    if 'hours' in tweet_processed or 'hrs' in tweet_processed:
        flag_5=True

    if '@' in tweet_processed:
        flag_6=True

    print(f"Tweet length:{len(tweet_processed)}")


    if flag_3==True or flag_4==True:
        
        if flag_5==True or flag_3==True:
            print("Flag 3 and 5 verified")
            if flag_1==True and flag_2==True:
                print("Flag 1 and 2 verified")
                if flag_6==True:
                       print("Flag 6 verified")
                       if flag_11==True and flag_12==True:
                        print("Flag 11 and 12 verified")
                        return True
                        print(f"Tweet length:{len(tweet_processed)}")
    else:
        return False


# ================ MAIN ======================

for filename in glob.glob("*.csv"):

    file=pd.read_csv(f'{filename}')

    tweets=[] # Init tweets buffer
    tweet_ids=[]

    for index, row in file.iterrows():

        user_id=row['author_id']

        #print(f"Checking user id:{user_id}")
        tweet_text=row['text']
        tweets.append(tweet_text)
        user_name=row['author.username']
        tweet_id=row['id']
        tweet_ids.append(tweet_id)
        followers=row['author.public_metrics.followers_count']

    follower_check=check_if_user_has_enough_followers(followers)

    if follower_check==True:
            for i,j in zip(tweets,tweet_ids):
                print(f"Checking user_id:{user_id} and tweet id:{i}")
                print(f"{i}")
                check_tweet=check_if_tweet_is_promotion(i)
                if check_tweet==True:
                    # User is account promoter
                    print("User is account promoter")
                    #time.sleep(5)
                    file=open("account_promoters.csv","a",encoding="utf-8")
                    file.write(f"{user_id},{user_name},{followers},{j},{i}\n") # j= tweet id, i=tweet text
                    file.close()
                    break
                else:
                    pass





