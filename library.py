import sqlite3

conn = sqlite3.connect('library.db')
print("Connected to library.db");
cursor = conn.cursor()

"""
Executes CREATE TABLE statement
connection: sqlite3 database connection
tableStatement: SQL statement in string
"""
def createTable(connection, tableStatement):
    try:
        assert (tableStatement != "")
        cur = connection.cursor()
        cur.execute(tableStatement)
    except:
        print("Error in table statement")

"""
Runs query on database
connection: sqlite3 database connection
queryStatement: SQL statement in string
"""
def runQuery(connection, queryStatement):

    try:
        cur = connection.cursor()
        cur.execute(queryStatement)
        results = cur.fetchall()
        print(results)
    except:
        print("Error running query")






