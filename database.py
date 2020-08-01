#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

class Database:

    def __init__(self,dbname="newdb.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

        #create database method , person is the chatid so the database items are individual to each user
    def create_database(self):
        with self.conn:
            command = "CREATE TABLE IF NOT EXISTS items(person integer,desctiption text)"
            self.conn.execute(command)

    def insert_into_database(self,item,person):
        with self.conn:
            command = "INSERT INTO items (person ,desctiption) VALUES (?,?)"
            tuple_value = (person,item)
            self.conn.execute(command,tuple_value)

    def delete_from_database(self,item,person):
        with self.conn:
            command = "DELETE FROM items  WHERE desctiption = (?) and person = (?)"
            tuple_value = (item ,person )
            self.conn.execute(command,tuple_value)

    def purge_database(self,person):
        with self.conn:
            command = "delete from items where person = (?)"
            tuple_value = (person,)
            self.conn.execute(command,tuple_value)

    #To fetch the last item from the database
    def select_one_from_database(self,person):
        command = "SELECT * FROM items where person=(?)"
        tuple_value = (person,)
        try:
            newlist=[item[1] for item in self.conn.execute(command,tuple_value).fetchall()]
            return newlist[-1]
        except IndexError:
            print("The database is empty already")
    #To fetch the list of items belonging to a person
    def select_all_from_database(self,person):
        command = "SELECT * FROM items where person=(?)"
        tuple_value = (person,)
        try:
            #return self.conn.execute(command).fetchall()
            newlist=[item[1] for item in self.conn.execute(command,tuple_value).fetchall()]
            return newlist
        except IndexError:
            return "The database is empty already"


'''
SAMPLE INSTANCE CREATING FOR CHECKING BEFORE IMPLEMENTING THE CLASS IN BOT PROGRAM
a=Database()
a.purge_database()
a.create_database()
a.insert_into_database("list",123)
a.insert_into_database("list2",456)
a.insert_into_database("list one ",123)
print(a.select_all_from_database(123))
print(a.select_all_from_database(456))
a.delete_from_database("list2",456)
print(a.select_all_from_database(123))
print(a.select_all_from_database(456))
'''
