import requests
import os
import logging

def fetchStats(gameId):
    logging.info(gameId )
    url = f"https://v2.nba.api-sports.io/players/statistics?game={gameId}"
    headers = {
        'x-rapidapi-host': "v2.nba.api-sports.io",
        'x-rapidapi-key': os.environ.get("API-KEY")
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None
    
def fetchGames():
    url = f"http://get-nba-games-production.up.railway.app/getTodays"
    headers = {
        'Authorization': os.environ.get("AUTH")
    }
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None