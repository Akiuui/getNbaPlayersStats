from flask import jsonify, abort
from pymongo import MongoClient, UpdateOne
from fetchers import fetchGames, fetchStats
from formatter import getIds, formatStats
import os
import logging
import datetime

def getTodaysDate():
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")
    return DTformatted

def ConnectToMongo():
    try:
        client = MongoClient(os.environ.get("MONGO_KEY"), tls=True)
    except Exception as e:
        logging.info(f"There has been an exception! {e.args}")
        return jsonify({"error": "Could not connect to MongoDB"}), 500

    return client

def GetStatByParam(paramQuery, value):

    logging.info("Trying to connect to mongo")
    client = ConnectToMongo()
    logging.info("Successfuly connected to mongo")
    
    db = client["NbaGames"]
    collection = db["NbaStats"]

    logging.info(f"Value of the query value: {value}")
    stat = collection.find({paramQuery: int(value)})
    stat = list(stat)
    if stat:
        logging.info("Successfully found the stat")

        if len(stat)==1:
            stat = stat[0]

        return stat
    else:
        logging.info("Stat not found, stat=None")
        abort(404, description="Stat not found, stat=None")

def fetchAndSaveStats():
    logging.info("Trying to connect to Mongo")
    client = ConnectToMongo()
    logging.info("Succesfully connected to mongoDb")

    db = client["NbaGames"]
    collection = db["NbaStats"]

    logging.info("Fetching todays games")
    games = fetchGames()
    gameIds = getIds(games["res"])
    
    stats = []
    logging.info("Fetching todays stats")
    for id in gameIds:
        stat = fetchStats(id)
        formattedStat = formatStats(stat)
        stats.extend(formattedStat)

    operations = [
        UpdateOne({"_id": stat["_id"]}, {"$set": stat}, upsert=True) for stat in stats
    ]

    logging.info("Trying to bulk write to mongo")
    # Perform bulk update (insert new, overwrite existing)
    if operations:
        result = collection.bulk_write(operations)
        logging.info(f"Matched: {result.matched_count}, Upserted: {result.upserted_count}, Modified: {result.modified_count}")

    return [result.matched_count, result.upserted_count, result.modified_count]

    

