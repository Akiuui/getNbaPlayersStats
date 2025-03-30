from flask import Blueprint, jsonify, request, abort
from services import fetchAndSaveStats, GetStatByParam
import logging
import os

stats_bp = Blueprint("stats", __name__)

@stats_bp.before_request
def before():

    gameId = request.args.get('gameId', "")
    playerId = request.args.get('playerId', "")

    if gameId == "":
        logging.info(f"The arg 'gameId' is not entered")
    elif gameId.isdigit():
        logging.info(f"Value of arg 'gameId' is: {gameId}")
    else:
        abort(400, description="gameId query must contain only digits")
        
    if playerId == "":
        logging.info(f"The arg 'playerId' is not entered")
    elif playerId.isdigit():
        logging.info(f"Value of arg 'playerId' is: {playerId}")
    else:
        abort(400, description="playerId query must contain only digits")
        
@stats_bp.route("/getStat", methods=["GET"])
def getStat():

    gameId = request.args.get('gameId', "")
    playerId = request.args.get('playerId', "")

    if gameId == "" or playerId == "":
        abort(400, description="Missing 'gameId' or 'playerId' parameter")

    statId = int(playerId+gameId)

    result = GetStatByParam("_id",statId)

    return jsonify(result), 200

@stats_bp.route("/getStatFromGame", methods=["GET"])
def getStatsFromGame():

    gameId = request.args.get('gameId', "")

    if gameId == "":
        abort(400, description="Missing 'gameId'")

    result = GetStatByParam("gameId", gameId)

    return jsonify(result), 200