import sqlite3

conn = sqlite3.connect('library.db')
print("Connected to library.db");
cur = conn.cursor()

"""
Executes CREATE TABLE statement
connection: sqlite3 database connection
tableStatement: SQL statement in string
"""
def createSchema():
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
    
def insertInto():
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


def generateQuery(attributes, tables, condition):
    attributeList = ', '.join(attributes)
    table = ' JOIN '.join(tables)

    result = "SELECT ", attributeList, "FROM ", table, "WHERE", condition

if __name__ == "__main__":
    createSchema()
    insertInto()

    cur.execute("SELECT * FROM Items")
    rows = cur.fetchall()

    print(rows)