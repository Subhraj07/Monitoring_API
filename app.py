from flask import Flask, request
import json
import logging
from flask_jsonpify import jsonify
from pyspark.sql import SparkSession


def init_spark_session():
    spark = SparkSession \
        .builder \
        .appName("test") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()
    return spark


# Init spark session and load libraries
spark = init_spark_session()

from flask import Blueprint

main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
# def top_ratings(user_id, count):
#     logger.debug("User %s TOP ratings requested", user_id)
#     top_ratings = recommendation_engine.get_top_ratings(user_id, count)
#     return json.dumps(top_ratings)

@main.route("/edl_log", methods=["GET"])
def get_edl_log():
    df = spark.read.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/monitoring") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "monitoring.edl_log") \
        .option("user", "root") \
        .option("password", "cloudera") \
        .load()

    results = df.select("system_name", "status", "logtime", "data_path").toJSON().map(lambda j: json.loads(j)).collect()
    return jsonify(results)


@main.route("/edl_table", methods=["GET"])
def get_edl_table():
    df = spark.read.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/monitoring") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "monitoring.edl_table") \
        .option("user", "root") \
        .option("password", "cloudera") \
        .load()

    results = df.toJSON().map(lambda j: json.loads(j)).collect()
    return jsonify(results)


@main.route("/taskexecution", methods=["GET"])
def get_task_execution():
    df = spark.read.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/monitoring") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "monitoring.taskexecutionhistory") \
        .option("user", "root") \
        .option("password", "cloudera") \
        .load()

    results = df.toJSON().map(lambda j: json.loads(j)).collect()
    return jsonify(results)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
