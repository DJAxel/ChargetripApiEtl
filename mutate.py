import os
import json

filepath = r"/home/axel/Documents/electralign-data/stations-all.json"
newData = {"data": {"stationList": []}}

if os.path.isfile(filepath):
    with open(filepath, 'r') as file:
        print("File opened")
        data = json.load(file)
        print("Data loaded")
        newData["data"]["stationList"] = data
        print("new data set")

filepath = r"/home/axel/Documents/electralign-data/stations-all-fixed.json"
with open(filepath, 'w') as file:
    print("New file opened")
    json.dump(newData, file)
    print("Done saving data")
