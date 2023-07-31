import sqlite3

print("hello library")

def create_schema():
    # Connect to the database or create it if it doesn't exist
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()

    # Create the Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Items (
            itemID INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            type TEXT,
            available INTEGER
        )
    ''')

    # Create the Borrows table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Borrows (
            personIDFK_Person INTEGER,
            itemIDFK_Items INTEGER,
            borrowDate TEXT,
            dateDue TEXT,
            returnDate TEXT,
            fineAmount REAL,
            FOREIGN KEY(personIDFK_Person) REFERENCES Person(personID),
            FOREIGN KEY(itemIDFK_Items) REFERENCES Items(itemID)
        )
    ''')

    # Create the Person table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            personID INTEGER PRIMARY KEY,
            firstName TEXT,
            lastName TEXT,
            birthDate TEXT
        )
    ''')

    # Create the Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employeeID INTEGER PRIMARY KEY,
            firstName TEXT,
            lastName TEXT,
            personIDFK_Person INTEGER,
            FOREIGN KEY(personIDFK_Person) REFERENCES Person(personID)
        )
    ''')

    # Create the Participates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Participates (
            eventIDFK_Event INTEGER,
            personIDFK_Person INTEGER,
            FOREIGN KEY(eventIDFK_Event) REFERENCES Event(eventID),
            FOREIGN KEY(personIDFK_Person) REFERENCES Person(personID)
        )
    ''')

    # Create the Event table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Event (
            eventID INTEGER PRIMARY KEY,
            type TEXT,
            audience TEXT,
            location TEXT
        )
    ''')

    # Create the FutureItems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FutureItems (
            fID INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            type TEXT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schema()
