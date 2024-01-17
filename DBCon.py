from __future__ import annotations

import logging
import sqlite3
from datetime import datetime


class DBCon:
    __instance: DBCon | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if hasattr(self, "con"):
            return
        self.con = sqlite3.connect("db.sqlite3")
        logging.warning("DATABASE CONNECTED SUCCESSFULLY")

    def __del__(self):
        self.con.close()
        logging.warning("DATABASE DISCONNECTED SUCCESSFULLY")

    def add_record(self, path):
        query = """INSERT INTO file_saves (datetime, path) VALUES (?, ?)"""
        params = (datetime.now(), path)

        logging.info(f"New record, params: {params}")

        self.con.execute(query, params)
        self.con.commit()

    def get_records(self, amount):
        query = """SELECT * FROM file_saves
         ORDER BY id DESC
         LIMIT ?"""
        params = (amount, )

        logging.info(f"Fetched last {amount} records")

        return self.con.execute(query, params).fetchall()


    # DESC убрать если не по порядку будет сохраняться



