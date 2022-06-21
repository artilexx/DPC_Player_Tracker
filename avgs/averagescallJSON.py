import requests
import json
from proIDs import pos1, pos2, pos3, pos4, pos5
import time

def createavgs(account_id, filename):
    statscall = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches")
    statsdata  = json.loads(statscall.text)

    kills = 0
    deaths = 0
    gpm = 0
    xpm = 0
    herodamage = 0
    towerdamage = 0
    lasthits = 0
    
    # get numbers for each stat from API call
    for match in statsdata:
        if type(match) == dict:
            kills = match.get("kills")
            deaths = match.get("deaths")
            gpm = match.get("gold_per_min")
            xpm = match.get("xp_per_min")
            herodamage = match.get("hero_damage")
            towerdamage = match.get("tower_damage")
            lasthits = match.get("last_hits")
    
    print(player, kills, deaths)

    with open(filename) as json_file:
        avgdict = json.load(json_file)
        avgdict.get("kdlist").append(kills/deaths)
        avgdict.get("gpmlist").append(gpm/20)
        avgdict.get("xpmlist").append(xpm/20)
        avgdict.get("hdlist").append(herodamage/20)
        avgdict.get("tdlist").append(towerdamage/20)
        avgdict.get("lhlist").append(lasthits/20)

    
    open(filename,"w").close()
    json_file  = open(filename,"w")
    json.dump(avgdict, json_file, indent  = 4)

    time.sleep(1) #api limits calls per minute


for player in pos1:
    createavgs(pos1.get(player), "avgs\pos1avgs.json")

for player in pos2:
    createavgs(pos2.get(player), "avgs\pos2avgs.json")

for player in pos3:
    createavgs(pos3.get(player), "avgs\pos3avgs.json")

for player in pos4:
    createavgs(pos4.get(player), "avgs\pos4avgs.json")

for player in pos5:
    createavgs(pos5.get(player), "avgs\pos5avgs.json")