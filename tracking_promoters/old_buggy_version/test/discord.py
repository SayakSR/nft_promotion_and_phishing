import pandas as pd
import json
import ast




def discord_slicer(s, delim): #Slice the URL string to extract invite code
    return s.partition(delim)[2]

def discord_get_follower_count(invite_code,timestamp):
    import requests
    from bs4 import BeautifulSoup as bs
    import json

    page = requests.get(f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true")
    soup = bs(page.content,features="html.parser")

    # Saving backup

    file=open(f"discord_metadata/{invite_code}_{timestamp}.json","w")
    file.write(str(soup))
    file.close()

    data = json.loads(str(soup))
    return data['approximate_member_count']




def discord_driver(timestamp):
    df=pd.read_csv("princess.csv")

    for index,row in df.iterrows():
        url=row['entities.urls']
        try:
            url_json=ast.literal_eval(url) # Converts raw string into dictionary
            
            expanded_url=(url_json[0]['expanded_url'])

            if "discord" in expanded_url:
                #print(expanded_url)
                expanded_url=expanded_url.replace("https://", "")
                print(expanded_url)
                invite_code=discord_slicer(expanded_url, "/")
                print(invite_code)
                follower_count=discord_get_follower_count(invite_code,timestamp)
                print(f"Follower count:{follower_count}")

                # Getting followers in the discord channel

            
        except Exception as e:
            print(e)
