import pandas as pd
import json
import ast




def discord_slicer(s, delim): #Slice the URL string to extract invite code
    return s.partition(delim)[2]

def discord_get_data(invite_code):
    import requests
    from bs4 import BeautifulSoup as bs
    import json

    page = requests.get(f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true")
    soup = bs(page.content,features="html.parser")

    # Saving backup

    # file=open(f"discord_metadata/{invite_code}_{timestamp}.json","w")
    # file.write(str(soup))
    # file.close()
    data = json.loads(str(soup))
    promotee_id=data['guild']['id'] # promotee_id

    promotee_name=invite_code # promotee name

    promotee_user_name=data['guild']['name'] # promotee_user_name

    try:
        promotee_bio=data['guild']['welcome_screen']['description'] # bio
    except:
        promotee_bio="None"

    promotee_follower_count=data['approximate_member_count'] 


    

    return promotee_name,promotee_id,promotee_user_name,promotee_bio,promotee_follower_count




def discord_driver(expanded_url,timestamp):

    if 'http://' in expanded_url:
        expanded_url=expanded_url.replace("http://", "")
    elif 'https://' in expanded_url:
        expanded_url=expanded_url.replace("https://", "")
    
    print(expanded_url)
    invite_code=discord_slicer(expanded_url, "/")
    if "invite" in invite_code:
        invite_code=invite_code.replace("invite/", "")

    print(invite_code)
    output=discord_get_data(invite_code)
    return output

    # Getting followers in the discord channel

    

# def discord_driver_raw(timestamp): # To test without any dependencies
#     df=pd.read_csv("princess.csv")

#     for index,row in df.iterrows():
#         url=row['entities.urls']
#         try:
#             url_json=ast.literal_eval(url) # Converts raw string into dictionary
            
#             expanded_url=(url_json[0]['expanded_url'])

#             if "discord" in expanded_url:
#                 #print(expanded_url)
#                 expanded_url=expanded_url.replace("https://", "")
#                 print(expanded_url)
#                 invite_code=discord_slicer(expanded_url, "/")
#                 print(invite_code)
#                 follower_count=discord_get_follower_count(invite_code,timestamp)
#                 print(f"Follower count:{follower_count}")

#                 # Getting followers in the discord channel

            
#         except Exception as e:
#             print(e)