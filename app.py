from flask import Flask
import logging
from flask_jsonpify import jsonify
from flask import Blueprint
from read_db import *

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
# def top_ratings(user_id, count):
#     logger.debug("User %s TOP ratings requested", user_id)
#     top_ratings = recommendation_engine.get_top_ratings(user_id, count)
#     return json.dumps(top_ratings)


@main.route("/edl_table", methods=["GET"])
def get_edl_log():
    df = read_data()
    return jsonify(df.to_json(orient='records'))


@main.route("/edl_table/<int:days>", methods=["GET"])
def get_filtered_edl(days):
    df = read_data_days(days)
    return jsonify(df.to_json(orient='records'))


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
