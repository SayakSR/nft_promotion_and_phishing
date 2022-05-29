# Third party imports

import os
import pandas as pd

# Own imports

from drivers.screenshot import take_screenshot

# ==== Begin ==== 

#nft_keywords=['#NFT', '#NFTs', '#NFTArt', '#NFTGiveaway', '#NFTGiveaways', '#NFTdrop', '#NFTCommunity', '#NFTCollection']
nft_keywords=['#NFTGiveaway']





for i in nft_keywords:
    
    cmd_fetch="twarc2 search --limit 3500"+ " '"+str(i)+"' output/"+str(filename)+".json" # Invokes twarc to fetch tweets using the academic API
    cmd_convert_to_csv="twarc2 csv "+"output/"+str(filename)+".json"+" output/"+str(filename)+".csv" # Parses twarc json data to csv format 
    os.system(cmd_fetch)
    os.system(cmd_convert_to_csv)
    #print(cmd_convert_to_csv)

    








