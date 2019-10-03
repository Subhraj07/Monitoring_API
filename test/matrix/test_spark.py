from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp
from config.Config import Config


def init_spark_session():
    spark = SparkSession \
        .builder \
        .appName(Config.app_name) \
        .config("spark.driver.memory", Config.driver_memory) \
        .config("spark.executor.memory", Config.executor_memory) \
        .getOrCreate()
    return spark


spark = init_spark_session()


def get_edl_log():
    df = spark.read.format("jdbc") \
        .option("url", "jdbc:mysql://localhost:3306/monitoring") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "monitoring.edl_log") \
        .option("user", "root") \
        .option("password", "cloudera") \
        .load()

    results = df.select("system_name", "status", "log_time", "data_path")
    results = results.withColumn("log_time", to_timestamp(df.log_time, 'yyyy-MM-dd HH:mm:ss'))
    return results


print(get_edl_log().printSchema())

spark.stop()
