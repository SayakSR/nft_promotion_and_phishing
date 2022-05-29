# Third party imports

import os
import pandas as pd

# First party imports

from drivers.date_time_stamp import *
from drivers.countdown import *
from drivers.directory_handler import create_directory
from drivers.process_tweets import process_tweet

# ==== Begin ==== 

#nft_keywords=['#NFT', '#NFTs', '#NFTArt', '#NFTGiveaway', '#NFTGiveaways', '#NFTdrop', '#NFTCommunity', '#NFTCollection']
fetch_keywords=['dm for promotions']

while 1: # Infinite run

  

    for i in fetch_keywords:

        fetch_keyword=str(i)
        datestamp=fetch_date()
        timestamp=fetch_time()

        fetch_dir=fetch_keyword.replace(" ", "_")
        create_directory(fetch_dir,datestamp)

        cmd_fetch=f'twarc2 search --limit 100 "{fetch_keyword}" raw_output/{fetch_dir}/{datestamp}/{timestamp}.json'

        print(cmd_fetch)
        cmd_convert_to_csv=f'twarc2 csv raw_output/{fetch_dir}/{datestamp}/{timestamp}.json raw_output/{fetch_dir}/{datestamp}/{timestamp}.csv '
        os.system(cmd_fetch)
        os.system(cmd_convert_to_csv)

        filepath=f"raw_output/{fetch_dir}/{datestamp}/{timestamp}.csv"
        print(filepath)


        process_tweet(filepath)
        countdown(300)

    








