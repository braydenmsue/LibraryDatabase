import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect('library.db')

dbAttributes = {'Items': ['itemID', 'title', 'author', 'type', 'available'],
                'Borrows': ['personID', 'itemID', 'borrowDate', 'dateDue', 'returnDate', 'fineAmount'],
                'Person': ['personID', 'firstName', 'lastName', 'birthDate'],
                'Employee': ['employeeID', 'firstName', 'lastName', 'personID'],
                'Participates': ['eventID', 'personID'],
                'Event': ['eventID', 'type', 'audience', 'location'],
                'Orders': ['orderID', 'employeeID', 'fID'],
                'FutureItems': ['fID', 'title', 'author', 'type']
                }

def checkSchemaExists(cur):
    # Define the list of tables that should exist in the schema
    required_tables = [
        "Items",
        "Borrows",
        "Person",
        "Employee",
        "Participates",
        "Event",
        "Orders",
        "FutureItems"
    ]

    # Check if each required table exists in the database
    for table in required_tables:
        cur.execute(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}'")
        table_exists = cur.fetchone()[0]
        if not table_exists:
            return False

    return True

"""
Executes CREATE TABLE statement
connection: sqlite3 database connection
tableStatement: SQL statement in string
"""
def createSchema():
    conn = sqlite3.connect('library.db')
    cur = conn.cursor()
    if checkSchemaExists(cur):
        print("Schema already created.")
    else:
        cur.execute('''
                CREATE TABLE IF NOT EXISTS Items (
                    itemID CHAR(11) PRIMARY KEY,
                    title CHAR(50),
                    author CHAR(50),
                    type CHAR(50),
                    available INTEGER
                )    
            ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Borrows (
            borrowID INTEGER PRIMARY KEY,
            personID CHAR(11),
            itemID CHAR(11),
            borrowDate DATE,
            dateDue DATE,
            returnDate DATE,
            fineAmount REAL,
            FOREIGN KEY (personID) REFERENCES Person(personID),
            FOREIGN KEY (itemID) REFERENCES Items(itemID)
            )
        ''')
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            personID CHAR(11) PRIMARY KEY,
            firstName CHAR(20),
            lastName CHAR(20),
            birthDate DATE
        )
    ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employeeID CHAR(11) PRIMARY KEY,
            firstName CHAR(20),
            lastName CHAR(20),
            personID CHAR(11),
            FOREIGN KEY (personID) REFERENCES Person(personID)
        )
    ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Participates (
            eventID CHAR(11),
            personID CHAR(11),
            FOREIGN KEY (eventID) REFERENCES Event(eventID),
            FOREIGN KEY (personID) REFERENCES Person(personID),
            PRIMARY KEY (eventID, personID)
        )
    ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Event (
            eventID CHAR(11) PRIMARY KEY,
            type CHAR(50),
            audience CHAR(50),
            date DATE,
            location CHAR(50)
        )
    ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                orderID CHAR(11) PRIMARY KEY,
                employeeID CHAR(11),
                fID CHAR(11),
                FOREIGN KEY (employeeID) REFERENCES Employee(employeeID),
                FOREIGN KEY (fID) REFERENCES FutureItems(fID)
            )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS FutureItems (
            fID CHAR(11) PRIMARY KEY,
            title CHAR(50),
            author CHAR(50),
            type CHAR(50)
            )
        ''')
        print("created tables")
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
    #print("Inserted items into Items")

    cur.execute('''
        INSERT OR IGNORE INTO Person(personID, firstName, lastName, birthDate)
        VALUES  ('1001', 'John', 'Doe', '1985-05-10'),
                ('1002', 'Jane', 'Smith', '1990-12-15'),
                ('1003', 'Michael', 'Johnson', '1988-07-22'),
                ('1004', 'Emily', 'Williams', '1995-03-08'),
                ('1005', 'Daniel', 'Brown', '1982-09-30'),
                ('1006', 'Olivia', 'Jones', '1998-11-25'),
                ('1007', 'William', 'Miller', '1989-06-18'),
                ('1008', 'Sophia', 'Davis', '1993-04-12'),
                ('1009', 'David', 'Garcia', '1986-02-28'),
                ('1010', 'Isabella', 'Martinez', '1991-08-05'),
                ('1011', 'Ella', 'Kim', '1997-09-20'),
                ('1012', 'Aiden', 'Nguyen', '1984-11-15'),
                ('1013', 'Chloe', 'Li', '1992-07-12'),
                ('1014', 'Ethan', 'Tanaka', '1987-03-25'),
                ('1015', 'Emma', 'Chen', '1994-06-02')
    ''')
    #print("Inserted records into Person")

    cur.execute('''
        INSERT OR IGNORE INTO Employee(employeeID, firstName, lastName, personID)
        VALUES  ('2001', 'John', 'Doe', '1001'),
                ('2002', 'Jane', 'Smith', '1002'),
                ('2003', 'Michael', 'Johnson', '1003'),
                ('2004', 'Emily', 'Williams', '1004'),
                ('2005', 'Daniel', 'Brown', '1005')
    ''')
    #print("Inserted records into Employee")

    cur.execute('''
        INSERT OR IGNORE INTO Event(eventID, type, audience, date, location)
        VALUES ('2001', 'Book Launch', 'Children', '2023-07-31', 'Library Hall'),
                ('2002', 'Workshop', 'Teens', '2023-08-05', 'Conference Room'),
                ('2003', 'Reading Session', 'Adults', '2023-08-12', 'Main Reading Area'),
                ('2004', 'Author Talk', 'All', '2023-08-17', 'Auditorium'),
                ('2005', 'Storytelling', 'Children', '2023-08-20', 'Children Section'),
                ('2006', 'Workshop', 'Adults', '2023-08-25', 'Conference Room'),
                ('2007', 'Book Launch', 'All', '2023-08-30', 'Library Hall'),
                ('2008', 'Reading Session', 'Teens', '2023-09-02', 'Main Reading Area'),
                ('2009', 'Author Talk', 'Adults', '2023-09-07', 'Auditorium'),
                ('2010', 'Storytelling', 'Children', '2023-09-10', 'Children Section')
                ''')
    #print("Inserted records into Event")
    
    cur.execute('''
        INSERT OR IGNORE INTO FutureItems(fID, title, author, type)
        VALUES  ('3001', 'Lord of the Flies', 'William Golding', 'Fiction'),
                ('3002', 'The Plague', 'Albert Camus', 'Fiction'),
                ('3003', 'Tao Te Ching', 'Lao Tzu', 'Philosophy'),
                ('3004', 'The Art of War', 'Sun Tzu', 'Military'),
                ('3005', 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 'Computer Science'),
                ('3006', 'Clean Code', 'Robert C. Martin', 'Computer Science'),
                ('3007', 'Design Patterns', 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides', 'Computer Science'),
                ('3008', 'Introduction to Algorithms', 'Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein', 'Computer Science'),
                ('3009', 'Artificial Intelligence: A Modern Approach', 'Stuart Russell, Peter Norvig', 'Computer Science'),
                ('3010', 'Data Science from Scratch', 'Joel Grus', 'Computer Science')
                ''')
    #print("Inserted records into FutureItems")
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
    try:
        if id != '-1':
            condition = "WHERE itemID = '" + id + "';"
        else:
            condition = "WHERE title = '" + title + "' OR author = '" + author + "';"
        sql = "SELECT * FROM Items " + condition

        cur = connection.cursor()
        cur.execute(sql)
        results = cur.fetchall()

        displayTable(results, 'Items')
        return results
    except:
        print("Error running query")

def displayTable(records, tableName):
    try:
        table = pd.DataFrame(records, columns=dbAttributes[tableName])
        print("\n")
        topLine = "------------------------------  " + tableName + "  ------------------------------"
        print(topLine)
        print(table.to_string(index=False))
        print("\n")

    except:
        print("Error displaying data")


def findPersonID(connection, personID):
    cur = connection.cursor()
    sql = "SELECT personID FROM Person WHERE personID = '" + personID + "';"
    result = cur.execute(sql)
    if result == None:
        choice = input("""ID not found, would you like to
        (1) Register for an account
        (2) Restart
        (Any Other Key) Exit
        """)
        if choice == '1':
            pass
            # id = makeAccount()
            # findPersonID(connection, id)
        elif choice == '2':
            findPersonID(connection, input("ID: "))
        else:
            print("Exiting.")
            return False
    else:
        print("ID found.")
        return True



def borrowBook(connection, personID, itemID):

    borrowDate = datetime.today()
    dateDue = (borrowDate + timedelta(days=30)).strftime('%Y-%m-%d')
    borrowDate = borrowDate.strftime('%Y-%m-%d')

    try:
        sql = "INSERT INTO Borrows(" + ", ".join(dbAttributes['Borrows']) + ") "
        sql += "VALUES('" + personID + "', '" + itemID + "', '" + borrowDate + "', '" + dateDue + "', NULL, 0);"
        print(sql)
        cur = connection.cursor()
        cur.execute(sql)
        print("Item borrowed successfully\n")
        return dateDue
    except:
        print("Error borrowing item\n")
        return

def returnItem(connection, personID):
    cur = connection.cursor()
    if findPersonID(connection, personID):
        sql = "SELECT * FROM Borrows WHERE personID = '" + personID + "';"
        print("Your Borrowed Items:\n")
        result = cur.execute(sql)
        displayTable(result, 'Borrows')
        choice = input("ID of record you would like to return: ")
        sqlSelect = "SELECT * FROM Borrows WHERE borrowID = '" + choice + "';"
        resultFinal = cur.execute(sqlSelect)
        if resultFinal:
            sqlDrop = "DELETE FROM Borrows WHERE personID = '" + personID + "' AND borrowID = '" + resultFinal[0][0] + "';"
            cur.execute(sqlDrop)
            connection.commit()
            return True
        else:
            print("Invalid selection")
            return False

if __name__ == "__main__":
    createSchema()
    insertInto(conn)

    cur.execute("SELECT * FROM Person")
    rows = cur.fetchall()

    print(rows)