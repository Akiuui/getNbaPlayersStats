from flask import Blueprint, request, abort, jsonify
from services import fetchAndSaveStats
import logging
import os

populate_bp = Blueprint("populate", __name__)

@populate_bp.route("/saveTodays", methods=["POST"])
def populate():

    authKey = request.headers.get("Auth", "").strip()

    if not authKey or authKey != os.environ.get("AUTH").strip():
        abort(401, description="Unauthorized access, missing Auth header")

    logging.info("Passed the authorization")

    inserted = fetchAndSaveStats()

    return jsonify({"SUcces: ": f"Matched: {inserted[0]}, Upserted: {inserted[1]}, Modified: {inserted[2]}"})