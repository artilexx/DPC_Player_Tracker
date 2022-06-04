import psycopg2
from psycopg2 import sql
import requests
import json
import os

from ..proIDs import pos1, pos2, pos3, pos4, pos5


def InitializeTables():
    DATABASE = os.environ.get("DATABASE")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")

    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host="HOST", port="5432")
    print("Database connected successfully")
    cur = conn.cursor()
    roles = ["pos1", "pos2", "pos3", "pos4", "pos5"]

    try:
        for role in roles:
            cur.execute(
                sql.SQL('''DROP TABLE IF EXISTS {}''').format(sql.Identifier(role)))
            cur.execute(
                sql.SQL('''CREATE TABLE {}(
                    Kills INTEGER,
                    Deaths INTEGER,
                    GoldPerMin INTEGER,
                    XPPerMin  INTEGER,
                    HeroDamage INTEGER,
                    TowerDamage  INTEGER,
                    LastHits  INTEGER,
                    MatchID BIGINT,
                    PlayerID BIGINT
                );''').format(sql.Identifier(role)))
            print("Table for {} created successfully".format(role))
    except:
        print("Table failed to create")

    conn.commit()
    conn.close()
    

def createavgs(conn, cur, account_id, role):

    statscall = requests.get("https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches") 
    statsdata  = json.loads(statscall.text)

    for match in statsdata:
        if type(match) == dict:
            kills = match.get("kills")
            deaths = match.get("deaths")
            gpm = match.get("gold_per_min")
            xpm = match.get("xp_per_min")
            hd = match.get("hero_damage")
            td = match.get("tower_damage")
            lh = match.get("last_hits")
            match_id = match.get("match_id")
            try:
                query = sql.SQL('''INSERT INTO {} (
                    Kills,
                    Deaths,
                    GoldPerMin,
                    XPPerMin,
                    HeroDamage,
                    TowerDamage,
                    LastHits,
                    MatchID,
                    PlayerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier(role))
                cur.execute(query, (kills, deaths, gpm, xpm, hd, td, lh, match_id, account_id))
                conn.commit()
                print("Data succesfully inserted for match "  + str(match_id))
            except:
                print("Data failed to insert for match " + str(match_id))

        
InitializeTables()

conn = psycopg2.connect(database="d71oks8144g5gl", user="yarctttrmsbwrw", password="8ea649ad98eda35589c20e877787132edd310ffbd297bcaa2ac1efcaa17f619e",
host="ec2-54-147-33-38.compute-1.amazonaws.com", port="5432")
print("Database connected successfully")
cur = conn.cursor()

for player in pos1:
    createavgs(conn, cur, pos1.get(player), "pos1")

for player in pos2:
    createavgs(conn, cur, pos2.get(player), "pos2")

for player in pos3:
    createavgs(conn, cur, pos3.get(player), "pos3")

for player in pos4:
    createavgs(conn, cur, pos4.get(player), "pos4")

for player in pos5:
    createavgs(conn, cur, pos5.get(player), "pos5")
