

# Tags to search for
# nft hours follow
# nft hours retweet

import pandas as pd
import glob, os


def check_if_user_has_enough_followers(followers):
    threshold=9999 
    if int(followers)>threshold:
        return True
    else:
        return False

def check_if_tweet_is_promotion(tweet,followers):
    print("Executed")
    check_t=check_if_user_has_enough_followers(followers)
    if check_t==True:
        flag_follow=True
    else:
        flag_follow=False

    # Init flags at start of every tweet
    flag_1,flag_2,flag_3,flag_4,flag_5,flag_6=0,0,0,0,0,0

    import re
    word = 'fubar'
    value_dol_regex = re.compile(r'\$[0-9]+')
    value_jt_regex=re.compile(r'JT[0-9]+')

    tweet_processed=tweet.lower()

    if "|" in tweet_processed or '~' or 'idr' in tweet_processed:
        flag_1=True
        print("Yes flag 1 was caught")
    else:
        print("No flag 1")

    if value_dol_regex.search(tweet_processed) or value_jt_regex.search(tweet_processed) or '~' in tweet_processed or 'idr' in tweet_processed:
        flag_2=True
    else:
        print("No flag 2")

    if 'rt' in tweet_processed or 'retweet' in tweet_processed:
        flag_3=True
    if 'follow' in tweet_processed:
        flag_4=True

    if 'hours' in tweet_processed or 'hrs' in tweet_processed or 'mins' in tweet_processed:
        flag_5=True
    if '@' in tweet_processed:
        flag_6=True


    if flag_3==True or flag_4==True:
        
        if flag_5==True or flag_3==True:
            if flag_1==True and flag_2==True:
                if flag_6==True:
                        if flag_follow==True:
                                print("Returned true")
                                return True
    else:
        print("Returned false")
        return False


# ================ MAIN ======================

def filter_potential_promoters(filename):

    promoter_list=[]

    file=pd.read_csv(f'{filename}')

    tweets=[] # Init tweets buffer

    for index, row in file.iterrows():

        user_id=row['author_id']

        #print(f"Checking user id:{user_id}")
        tweet_text=row['text']
        tweets.append(tweet_text)
        tweet_id=row['id']
        user_name=row['author.username']
        followers=row['author.public_metrics.followers_count']
    
        check_tweet=check_if_tweet_is_promotion(tweet_text)
        if check_tweet==True:
            if user_id in promoter_list:  # Adding to list the user id which has been flagged as potentially account promoter by heuristic
                pass
            else:
                promoter_list.append(user_id)
        else:
            pass
    return promoter_list





