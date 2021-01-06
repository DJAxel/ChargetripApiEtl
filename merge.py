import os
import json

path = r"/home/axel/Documents/electralign-data/"
stations = []

for filename in sorted(os.listdir(path)):
    filepath = os.path.join(path, filename)
    if os.path.isfile(filepath):
        print(filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            stations += data


with open(path+'stations-all.json', 'w') as file:
    json.dump(stations, file)

print("Saved " + str(len(stations)) + " stations")
