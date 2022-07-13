import json
import glob, os

for file in glob.glob("*.json"):
	#print(f"Opening {file}")

	f = open(file)

	dict=json.load(f)
	for i in range(100):
		collection=dict["data"]["rankings"]["edges"][i]["node"]["slug"]
		print(collection)