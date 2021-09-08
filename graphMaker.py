import matplotlib.pyplot as plt
import json
import requests

graphFileName = input("graphFile: ")
graphFile1 = open(graphFileName, "r")
graphFile = json.load(graphFile1)

highest = graphFile["highestValue"]
startTime = graphFile["startTime"]
checkedStats = graphFile["bedwarsStatsToTrack"] + graphFile["skywarsStatsToTrack"] + graphFile["duelsStatsToTrack"]
uuids = graphFile["uuids"]

names = []

for m in range(len(uuids)):
    nameResponse = requests.get("https://api.mojang.com/user/profiles/" + uuids[m] + "/names")
    names.append(nameResponse.json()[-1]["name"])


for j in range(len(uuids)):
    for p in range(len(checkedStats)):
        lineLabel = names[j] + " " + checkedStats[p]

        x = []
        y = []

        for i in range(int(highest)):
            #print(i)
            #print(graphFile[str(i)][uuids[j]])
            x.append(graphFile[str(i)]["time"] - startTime)
            #print(x)
            y.append(graphFile[str(i)][uuids[j]][checkedStats[p]])
            #print(y)

        #print(x)
        #print(y)
        plt.plot(x, y, label=lineLabel)


plt.xlabel('Time')

plt.ylabel('online')

# giving a title to my graph
plt.title(graphFileName)

plt.legend()

plt.show()