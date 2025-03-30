def getIds(array):
    ids = []
    for ele in array:
        ids.append(ele["_id"])

    return ids
        

def formatStats(stats):
    stats = stats["response"]

    statsFormatted = []
    for stat in stats:
        del stat["team"]
        stat["gameId"] = stat["game"]["id"]
        del stat["game"]
        stat["playerId"] = stat["player"]["id"]
        del stat["player"]["id"]
        stat["_id"] = int(str(stat["playerId"])+str(stat["gameId"]))
        statsFormatted.append(stat)

    return statsFormatted