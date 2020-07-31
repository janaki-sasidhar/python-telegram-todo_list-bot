#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Database:

    def __init__(self,dbname="newdb.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def create_database(self):
        with self.conn:
            command = "CREATE TABLE IF NOT EXISTS items(desctiption text)"
            self.conn.execute(command)

    def insert_into_database(self,item):
        with self.conn:
            command = "INSERT INTO items (desctiption) VALUES (?)"
            tuple_value = (item,)
            self.conn.execute(command,tuple_value)

    def delete_from_database(self,item):
        with self.conn:
            command = "DELETE FROM items  WHERE desctiption = (?)"
            tuple_value = (item , )
            self.conn.execute(command,tuple_value)

    def purge_database(self):
        with self.conn:
            command = "delete from items"
            self.conn.execute(command)
    def select_one_from_database(self):
        command = "SELECT * FROM items"
        try:
            newlist=[item[0] for item in self.conn.execute(command).fetchall()]
            return newlist[-1]
        except IndexError:
            print("The database is empty already")

    def select_all_from_database(self):
        command = "SELECT * FROM items"
        try:
            #return self.conn.execute(command).fetchall()
            newlist=[item[0] for item in self.conn.execute(command).fetchall()]
            return newlist
        except IndexError:
            return "The database is empty already"


#a=Database()
#a.create_database()
#a.insert_into_database("list")
#print(a.select_all_from_database())