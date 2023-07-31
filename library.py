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

def insertData(connection, insertStatement):
    try:
        assert (insertStatement != "")
        cur = connection.cursor()
        cur.execute(insertStatement)
    except:
        print("Error inserting data")

def updateTable(connection, updateStatement):
    try:
        assert (updateStatement != "")
        cur = connection.cursor()
        cur.execute(updateStatement)
    except:
        print("Error updating table")


def deleteData(connection, deletionStatement):
    try:
        assert (deletionStatement != "")
        cur = connection.cursor()
        cur.execute(deletionStatement)
    except:
        print("Error deleting data")

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


# def generateQuery(attributes, tables, condition):
#     attributeList = ', '.join(attributes)
#     table = ' JOIN '.join(tables)
#
#     result = "SELECT ", attributeList, "FROM ", table, "WHERE", condition
