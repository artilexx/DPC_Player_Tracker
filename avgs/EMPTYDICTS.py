import json
emptydict = {
    "kdlist": [],
    "gpmlist": [],
    "xpmlist": [],
    "hdlist": [],
    "tdlist": [],
    "lhlist": []
}
for filename in ["avgs\pos1avgs.json","avgs\pos2avgs.json","avgs\pos3avgs.json","avgs\pos4avgs.json","avgs\pos5avgs.json"]:
    avgfile = open(filename,"w")
    json.dump(emptydict, avgfile, indent = 4)
    avgfile.close()