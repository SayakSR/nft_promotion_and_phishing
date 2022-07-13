import requests
from bs4 import BeautifulSoup as bs
import json

def discord():
    page = requests.get("https://discord.com/api/v9/invites/monopolondefi?with_counts=true&with_expiration=true")
    soup = bs(page.content,features="html.parser")

    print(soup)

    data = json.loads(str(soup))
    promotee_id=data['guild']['id'] # promotee_id

    

    promotee_user_name=data['guild']['vanity_url_code'] # promotee_user_name

    try:
        promotee_bio=data['guild']['welcome_screen']['description'] # bio
    except:
        promotee_bio="None"

    promotee_follower_count=data['approximate_member_count'] 

    return promotee_user_name,promotee_bio,promotee_follower_count


a=discord()
print(a[0])






