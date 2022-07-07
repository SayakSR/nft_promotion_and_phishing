import requests
from bs4 import BeautifulSoup as bs
import json

page = requests.get("https://discord.com/api/v9/invites/Etx2zDMCuQ?with_counts=true&with_expiration=true")
soup = bs(page.content,features="html.parser")

print(soup)

data = json.loads(str(soup))
print(data['approximate_member_count'])

