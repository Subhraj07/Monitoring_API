import configparser
import os


def spark_config(conf, conf_path):
    conf.read(conf_path)
    app_name = conf.get("SPARK", 'APP')
    driver_memory = conf.get("SPARK", 'DRIVER_MEMORY')
    executor_memory = conf.get("SPARK", 'EXECUTOR_MEMORY')
    master = conf.get("SPARK", 'MASTER')

    return app_name, master, driver_memory, executor_memory


def db_details(db, conf, conf_path):
    conf.read(conf_path)
    user = conf.get(db, 'USER')
    password = conf.get(db, 'PASSWORD')
    url = conf.get(db, 'URL')
    driver = conf.get(db, 'DRIVER')

    return user, password, url, driver


class Config:
    def __init__(self):
        pass

    dir_path = os.path.dirname(__file__)
    conf_path = os.path.join(dir_path, 'conf.ini')

    config = configparser.ConfigParser()
    user, password, url, driver = db_details("GPDB", config, conf_path)
    app_name, master, driver_memory, executor_memory = spark_config(config, conf_path)
