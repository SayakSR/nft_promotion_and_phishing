import json
import ast

f = open('collection.json')

# data = json.loads(f)

# print(len(data))

# # print(data[3])
# # # print(data[3]['id'])
# # # print(data[3]['username'])
# # # print(data[3]['description'])
# # # print(data[3]['url'])


raw_read=f.read() # Reads the collection response into raw string

data_dict=ast.literal_eval(raw_read) # Converts raw string into dictionary

print(data_dict["collection"]["primary_asset_contracts"][0]["external_link"]) 