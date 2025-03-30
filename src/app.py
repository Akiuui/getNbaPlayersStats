from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

from blueprints.stats import stats_bp
from blueprints.populate import populate_bp

load_dotenv()
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app.register_blueprint(stats_bp)
app.register_blueprint(populate_bp)

if __name__=="__main__":
    from waitress import serve
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8000))
    serve(app, host="0.0.0.0", port=port)