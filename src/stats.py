import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def initdb():
    database = r"/var/lib/grafana/stats.db"

    sql_create_stats_table = """ CREATE TABLE IF NOT EXISTS stats (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
									   label VARCHAR(50),
									   confidence FLOAT,
									   total_time FLOAT,
									   predict_time FLOAT,
									   t TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                                    ); """
    conn = create_connection(database)

    with conn:
        cur = conn.cursor()
        cur.execute(sql_create_stats_table)
        conn.commit()
    return conn


def insert_prediction(conn, prediction):
    sql = ''' INSERT INTO stats (label, confidence, total_time, predict_time)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, prediction)
    conn.commit()
    return cur.lastrowid