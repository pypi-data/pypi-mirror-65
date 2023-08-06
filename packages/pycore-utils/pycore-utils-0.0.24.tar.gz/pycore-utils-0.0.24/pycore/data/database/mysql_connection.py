# coding=utf-8
import pymysql

from pycore.data.entity import config


def get_conn(host=config.get("db", "db_host"),
             port=int(config.get("db", "db_port")),
             user=config.get("db", "db_user"),
             password=config.get("db", "db_pass"),
             db=config.get("db", "db_db"),
             charset=config.get("db", "db_charset"),
             cursorclass=pymysql.cursors.DictCursor):
    return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset,
                           cursorclass=cursorclass)
