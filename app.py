from flask import Flask, render_template, send_from_directory
import requests
import os
import json
from proIDs import pos1, pos2, pos3, pos4, pos5, idlist
import time

app = Flask(__name__)

def assigngrade(player, overall, playerwinrate):
    possiblegrades = ["S", "A", "B", "C", "D", "F"]
    weightings = {"kd": 0.1, "gpm": 0.1, "xpm": 0.1, "herodamage": 0.1, "towerdamage":0.1, "lasthits": 0.1, "winrate": 0.4}
    score = 0
    for i in range(len(player)):
        score += player[i]/overall[i] * list(weightings.values())[i]
    score += list(weightings.values())[6] * (playerwinrate)

    if score > 0.95:
        grade = "S"
    elif score > 0.9:
        grade = "A"
    elif score > 0.8:
        grade = "B"
    elif score > 0.7:
        grade = "C"
    elif score > 0.6:
        grade = "D"
    else: 
        grade = "F"

    if playerwinrate < 0.4 and grade != "F":
        grade = possiblegrades[possiblegrades.index(grade)+1]

    return grade

def getplayerstats(player):

    account_id = 0
    if player.lower() not in idlist and player.isnumeric() == False:
        return render_template("invalidplayer.html", error_message = "{} not found, player must be in dropdown list or be a account ID".format(player))
    if player.lower() in idlist:
        account_id = idlist[player.lower()]
    if player.lower() in pos1: #determine player role to compare to avgs
        role = "pos1"
    elif player.lower() in pos2:
        role = "pos2"
    elif player.lower() in pos3:
        role = "pos3"
    elif player.lower() in pos4:
        role = "pos4"
    elif player.lower() in pos5:
        role = "pos5"
    else:
        account_id = player
        role  = "pos3"

    params  = {
        "limit": 20 # limit calls to 20 matches
    }

    winratecall = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/wl", params = params)
    winratedata = json.loads(winratecall.text)
    statscall = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches")
    statsdata  = json.loads(statscall.text)

    if statsdata == []:
        return render_template("invalidplayer.html", playername = player, error_message = "Account ID not found. Expose match data must be enabled")


    # stats to be displayed on HTML
    kills = 0
    deaths = 0
    gpm = 0
    xpm = 0
    herodamage = 0
    towerdamage = 0
    lasthits = 0
    winrate = 0

    # get numbers for each stat from API call
    for match in statsdata:
        kills += match.get("kills")
        deaths += match.get("deaths")
        gpm += match.get("gold_per_min")
        xpm += match.get("xp_per_min")
        herodamage += match.get("hero_damage")
        towerdamage += match.get("tower_damage")
        lasthits += match.get("last_hits")
    # get winrate
    winrate = (winratedata["win"]*100)/(winratedata["lose"] + winratedata["win"])
    
    #calculate avgs
    with open(f"avgs/{role}avgs.json") as avgfile:
        avgdict = json.load(avgfile)
        kdavg = sum(avgdict.get("kdlist")) / len(avgdict.get("kdlist"))
        gpmavg = sum(avgdict.get("gpmlist")) / len(avgdict.get("gpmlist"))
        xpmavg = sum(avgdict.get("xpmlist")) / len(avgdict.get("xpmlist"))
        hdavg = sum(avgdict.get("hdlist")) / len(avgdict.get("hdlist"))
        tdavg = sum(avgdict.get("tdlist")) / len(avgdict.get("tdlist"))
        lhavg = sum(avgdict.get("lhlist")) / len(avgdict.get("lhlist"))

    
    statslist = [kills/deaths, gpm/20, xpm/20, herodamage/20, towerdamage/20, lasthits/20]
    avglist = [kdavg, gpmavg, xpmavg, hdavg, tdavg, lhavg]

    playergrade = assigngrade(statslist, avglist, winrate/100)

    #color for jinja
    green = "rgb(89, 187, 94);"
    if winrate > 50:
        winratecolor = green
    elif winrate < 50:
        winratecolor = "red"
    else: 
        winratecolor = "black"

    if kills/deaths > kdavg:
        kdcolor = green
    else: 
        kdcolor = "red"

    if gpm/20 > gpmavg:
        gpmcolor = green
    else:
        gpmcolor = "red"

    if xpm/20 > xpmavg:
        xpmcolor = green
    else:
        xpmcolor = "red"

    if herodamage/20 > hdavg:
        hdcolor = green
    else:
        hdcolor = "red"

    if lasthits/20 > lhavg:
        lhcolor = green
    else:
        lhcolor = "red"

    if towerdamage/20 > tdavg:
        tdcolor = green
    else:
        tdcolor = "red"
    
    dropdownoptions = sorted(list(idlist.keys()))

    return render_template('web.html', 
        kdfront = round(kills/deaths, 2), kdavg = round(kdavg, 2), kdcolor = kdcolor,
        gpmfront = round(gpm/20,2), gpmavg = round(gpmavg, 2), gpmcolor = gpmcolor,
        xpmfront = round(xpm/20,2), xpmavg = round(xpmavg, 2), xpmcolor = xpmcolor,
        herodamagefront = round(herodamage/20,2), hdavg = round(hdavg, 2), hdcolor = hdcolor,
        towerdamagefront = round(towerdamage/20,2), tdavg = round(tdavg, 2), tdcolor = tdcolor,
        lasthitsfront = round(lasthits/20,2), lhavg = round(lhavg, 2), lhcolor = lhcolor,
        winratefront = winrate, winratecolor = winratecolor,
        playergrade = playergrade,
        dropdownoptions = dropdownoptions,
        playername = player.capitalize())
    

@app.route('/', methods = ["GET"])
def homepage():
    return getplayerstats("Arteezy") #Homepage set to rtz


@app.route('/<playername>', methods = ["GET"])
def profile(playername): 
    return getplayerstats(playername.lower())

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
