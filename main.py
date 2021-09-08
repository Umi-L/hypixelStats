import requests
import time
import json

key = "77a6dfc6-609e-484b-bbc1-e5480e8083b6"

delayTime = 10

uuids = []

existingFile = input("ExistingFile: ")

if existingFile == "":
    newFileName = input("(without ext) NewFileName: ")
    startTime = round(time.time())
    file = newFileName + ".json"
    playersToTrack = input("(seperate with ',') users to track: ").split(",")
    statsToTrack = input("coustomStats y/n: ")
    if statsToTrack == "n":
        bedwarsStatsToTrack = ["final_kills_bedwars", "final_deaths_bedwars", "beds_lost_bedwars", "beds_broken_bedwars", "games_played_bedwars", "wins_bedwars", "losses_bedwars", "kills_bedwars", "deaths_bedwars"]
        skywarsStatsToTrack = ["kills", "deaths", "wins", "losses", "assists"]
        duelsStatsToTrack = ["kills", "deaths", "sumo_duel_wins", "sumo_duel_losses", "bridge_duel_wins", "bridge_duel_losses", "classic_duel_wins", "classic_duel_losses", "op_duel_wins", "op_duel_losses", "sw_duel_wins", "sw_duel_losses"]
        mmStatsToTrack = ["wins", "losses", "games"]
    else:
        print("--Coustom Stats--")
        bedwarsStatsToTrack = input("BedwarsStats (seperate with ','): ").split(",")
        skywarsStatsToTrack = input("BedwarsStats (seperate with ','): ").split(",")
        duelsStatsToTrack = input("BedwarsStats (seperate with ','): ").split(",")
        mmStatsToTrack = input("MurderMystery (seperate with ','): ").split(",")
        statsToTrack = statsToTrack.split(",")

    for i in range(len(playersToTrack)):
        uuidResponse = requests.get("https://api.mojang.com/users/profiles/minecraft/" + playersToTrack[i - 1])
        currentUUID = uuidResponse.json()["id"]
        uuids.append(currentUUID)

    with open(file, "w") as temp:
        data = {
            "startTime":startTime,
            "uuids":uuids,
            "bedwarsStatsToTrack":bedwarsStatsToTrack,
            "skywarsStatsToTrack": skywarsStatsToTrack,
            "duelsStatsToTrack": duelsStatsToTrack,
            "highestValue":0
        }
        json.dump(data, open(file, "w"))

    i = 0

else:
    with open(existingFile, "r") as temp1:
        temp = json.load(temp1)

        startTime = temp["startTime"]

        uuids = temp["uuids"]

        statsToTrack = temp["statsToTrack"]

        i = temp["highestValue"]

        file = existingFile



while True:
    graphData = {i:{
        "time":round(time.time())
    }}

    for y in range(len(uuids)):
        perams = {
            "key": key,
            "uuid": uuids[y-1]
        }

        response = requests.get("https://api.hypixel.net/player", perams)

        statsResponse = response.json()["player"]["stats"]
        bedwarsResponseJson = statsResponse["Bedwars"]
        skywarsResponseJson = statsResponse["SkyWars"]
        duelsResponseJson = statsResponse["Duels"]
        mmResponseJson = statsResponse["MurderMystery"]

        graphData[i][uuids[y - 1]] = {}


        for j in range(len(bedwarsStatsToTrack)):
            currentStat = bedwarsStatsToTrack[j-1]

            graphData[i][uuids[y-1]][currentStat] = bedwarsResponseJson[bedwarsStatsToTrack[j]]

        for j in range(len(skywarsStatsToTrack)):
            currentStat = skywarsStatsToTrack[j]

            graphData[i][uuids[y-1]][currentStat] = skywarsResponseJson[skywarsStatsToTrack[j]]

        for j in range(len(duelsStatsToTrack)):
            currentStat = duelsStatsToTrack[j]

            graphData[i][uuids[y-1]][currentStat] = duelsResponseJson[duelsStatsToTrack[j]]

        for j in range(len(mmStatsToTrack)):
            currentStat = mmStatsToTrack[j]

            graphData[i][uuids[y-1]][currentStat] = mmResponseJson[mmStatsToTrack[j]]


    with open(file, "r+") as k:
        data = json.load(k)
        data["highestValue"] = i+1
        data.update(graphData)
        k.seek(0)
        json.dump(data, k)

    print(time.time())

    i+=1
    time.sleep(delayTime)
