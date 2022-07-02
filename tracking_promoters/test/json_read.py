import json

f = open('example.json')

data = json.load(f)

print(len(data))

# print(data[3])
# # print(data[3]['id'])
# # print(data[3]['username'])
# # print(data[3]['description'])
# # print(data[3]['url'])
