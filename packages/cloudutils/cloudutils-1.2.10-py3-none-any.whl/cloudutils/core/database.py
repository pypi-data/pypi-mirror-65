# Copyright © 2020 Noel Kaczmarek
from contextlib import closing

import sqlite3
import uuid
import os


class Database(object):
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        self.file = file

    def connect(self):
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()

    def insert(self, values):
        command = 'INSERT INTO %s (user, firstname, lastname, username, password, gender, email, birthdate, adress, ' \
                  'rank) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);' % (
                      values[0], values[1], values[2], values[3], values[4],
                      values[5], values[6], values[7], values[8])

        self.execute(command)
        self.commit()

    def get(self):
        self.connect()
        return self.connection, self.cursor

    def query(self, sql, **kwargs):
        with closing(sqlite3.connect(self.file)) as con, con,  \
                closing(con.cursor()) as cur:
            cur.execute(sql)
            if kwargs.get('fetchone', False):
                return cur.fetchone()
            return cur.fetchall()

    def execute(self, command):
        self.cursor.execute(command)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
