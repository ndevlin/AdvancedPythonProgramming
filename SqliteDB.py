from io import BytesIO
import sqlite3
import pandas as pd
import os
import pickle
import collections
import unittest

# global database
gsqliteDB = None

# dummy class placeholder
class Dummy:
    def __init__(self,first,last):
        self.first = first
        self.last = last
        
# convert data to bytes
def to_bytes(data):
    # https://www.geeksforgeeks.org/pickle-python-object-serialization/
    import pickle
    return pickle.dumps(data)    

# convert file to binary
def to_blob(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# Connect to a dbase
def Connect(dbname,query):
    global gsqliteDB
    try:
        gsqliteDB = sqlite3.connect(dbname)
        print(f"Connected to: {dbname}")
        cursor = Execute( gsqliteDB, query )
        record = cursor.fetchall()
        print(f"Version is: {record}")
    except sqlite3.Error as error:
        print(f"Error {error} connecting to sqlite {dbname}")
    return 1

# execute a query
def Execute(db,query="",tup=()):
    try:
        print(f"Execute query: {query}")
        cursor = db.cursor()
        cursor.execute(query, tup)        
        db.commit()
        print(f"Query executed")
    except sqlite3.Error as error:
        print(f"Query error: {error}")
    return cursor

# Connect to a dbase
def Connect(dbname,query):
    global gsqliteDB
    try:
        gsqliteDB = sqlite3.connect(dbname)
        print(f"Connected to: {dbname}")
        cursor = Execute( gsqliteDB, query )
        record = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"Error {error} connecting to sqlite {dbname}")
        
# Delete a record
def Delete(db,query):
    try:
        Execute(db,query)
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)

# Search for record
def Search(db,query):
    result = None
    try:
        cursor = Execute(db,query)
        result = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"Failed to search from sqlite table {error}")
    return result

# Insert data
def Insert(db,query,tup):
    try:
        Execute(db,query,tup)
    except sqlite3.Error as error:
        print(f"Failed to insert: {error}")

# Select data
def Select(db,query):
    records = None
    try:
        cursor = Execute(db,query)
        records = cursor.fetchall()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    return records

# Table fields
def Table(db,query):
    try:
        Execute(db,query)
    except sqlite3.Error as error:
        print(f"Table exists: {error}")

# Update record
def Update(db,query,tup):
    try:
        Execute(db,query,tup)
    except sqlite3.Error as error:
        print(f"Failed to update sqlite table {error}")

# Disconnect         
def Shutdown(db,dbname):
    db.close()
    print(f"{dbname} closed")
    os.remove(dbname)    ## removing is optional
    return 0

class Test(unittest.TestCase):
    
    def test(self) :
        
        #connect  __enter__
        print('\n******* Connect *******')
        database = "CIS41b_.db"     
        dbname = 'Database'    
        _QueryS_ = f"SELECT sqlite_version()"
        Connect(database,_QueryS_)
        
        #table
        print('\n******* Table *******')
        _QueryS_ = f"CREATE TABLE {dbname} (id INTEGER PRIMARY KEY, name TEXT NOT NULL, photo TEXT NOT NULL UNIQUE, html TEXT NOT NULL UNIQUE)"     
        Table(gsqliteDB,_QueryS_)

        print('\n******* Insert *******')
        data = (2, "CO2", to_blob("Co2.png"), to_blob("Co2.html"))
        Insert(gsqliteDB,_QueryS_,data)
    
        print('\n******* Insert *******')
        dframe = pd.DataFrame([1,2,3,4])
        data = (4, "DataFrame", to_blob("Dataframe.jpg"), to_bytes(dframe))
        Insert(gsqliteDB,_QueryS_,data)

        #read
        print('\n******* ReadTable *******')
        _QueryS_ = f"SELECT * from Database"
        records = Select(gsqliteDB,_QueryS_)
        
        #search
        print('\n******* Search *******')
        value = "CO2"
        _QueryS_ = f"SELECT id FROM Database WHERE name == '{value}'"
        record = Search(gsqliteDB,_QueryS_)
        
        #update
        print('\n******* Update *******')
        _QueryS_ = f"UPDATE Database set html = ? where id = ?"
        data = ("OS.html",2)
        Update(gsqliteDB, _QueryS_, data)
        
        #delete
        print('\n******* Delete *******')
        id = 2
        _QueryS_ = f"DELETE from Database where id = {str(id)}"
        Delete(gsqliteDB,_QueryS_)
        
        #shut-down  __exit__
        print('\n******* Close *******')
        assert( Shutdown(gsqliteDB,database) == 0 )
    
# Test
if __name__=='__main__':
    unittest.main()