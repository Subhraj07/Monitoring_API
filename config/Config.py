import configparser
import os


def db_details(db, conf, conf_path):
    conf.read(conf_path)
    user = conf.get(db, 'USER')
    password = conf.get(db, 'PASSWORD')
    database = conf.get(db, 'DATABASE')
    host = conf.get(db, 'HOST')
    port = conf.get(db, 'PORT')

    return user, password, database, host, port


class Config:
    def __init__(self):
        pass

    dir_path = os.path.dirname(__file__)
    conf_path = os.path.join(dir_path, 'conf.ini')

    config = configparser.ConfigParser()
    user, password, database, host, port = db_details("GPDB", config, conf_path)
