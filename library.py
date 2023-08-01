import sqlite3
import pandas as pd
import os

filePath = os.path.join(os.getcwd(), "library.db")

"""
Executes CREATE TABLE statement
connection: sqlite3 database connection
tableStatement: SQL statement in string
"""
def createSchema():
    if os.path.exists(filePath):
        print("Schema already created.")
    else:
        conn = sqlite3.connect('library.db')
        cur = conn.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS Items (
                    itemID CHAR(11) PRIMARY KEY,
                    title CHAR(50),
                    author CHAR(50),
                    type CHAR(50),
                    available INTEGER
                )    
            ''')

        conn.commit()

    return
    
def insertInto(conn):
    cur = conn.cursor()
    cur.execute('''
                INSERT OR IGNORE INTO Items(itemID, title, author, type, available)
                VALUES  ('1001', 'Love You Forever', 'Robert Munsch', 'Children', 1),
                        ('1002', 'The Paper Bag Princess', 'Robert Munsch', 'Children', 1),
                        ('1003', 'The Lightning Thief', 'Rick Riordan', 'Fantasy', 1),
                        ('1004', 'The Sea of Monsters', 'Rick Riordan', 'Fantasy', 1),
                        ('1005', 'Diary of a Wimpy Kid', 'Jeff Kinney', 'Comedy', 1),
                        ('1006', 'Rodrick Rules', 'Jeff Kinney', 'Comedy', 1),
                        ('1007', 'Geronimo Stilton: Lost Treasure of the Emerald Eye', 'Geronimo Stilton', 'Adventure', 1),
                        ('1008', 'Geronimo Stilton: The Curse of the Cheese Pyramid', 'Geronimo Stilton', 'Adventure', 1),
                        ('1009', 'Pigs', 'Robert Munsch', 'Children', 1),
                        ('1010', 'The Battle of the Labyrinth', 'Rick Riordan', 'Fantasy', 1)
                ''')
    print("Inserted items data")
    conn.commit()

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

def capitalizeWords(phraseString):
    wordList = phraseString.split(' ')
    wordListC = [word.capitalize() for word in wordList]
    result = ' '.join(wordListC)

    return result


"""
Runs query Items table by title and author
connection: sqlite3 database connection
queryStatement: SQL statement in string
"""
def searchItems(connection, title, author, id = '-1'):

    condition = ""
    attributes = ['ID', 'Title', 'Author', 'Type', 'Available']
    try:
        if id != '-1':
            condition = "WHERE itemID = '" + id + "';"
        else:
            condition = "WHERE title = '" + title + "' OR author = '" + author + "';"
        sql = "SELECT * FROM Items " + condition
        print(sql)

        cur = connection.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        table = pd.DataFrame(results, columns=attributes)
        print("-----------------------------------------------------------")
        print(table.to_string(index=False))
        print("-----------------------------------------------------------")

        return results
    except:
        print("Error running query")


if __name__ == "__main__":
    createSchema()
    insertInto()

    cur.execute("SELECT * FROM Items")
    rows = cur.fetchall()

    print(rows)