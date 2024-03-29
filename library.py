import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# Dictionary (key = table name, value = list of attributes)
# Primarily used to generate DataFrames, but comma separated strings also formed via ", ".join(dbAttributes['tableName']
dbAttributes = {'Items': ['itemID', 'title', 'author', 'type', 'available'],
                'Borrows': ['borrowID', 'personID', 'itemID', 'borrowDate', 'dateDue', 'returnDate', 'fineAmount'],
                'Person': ['personID', 'firstName', 'lastName', 'birthDate'],
                'Employee': ['employeeID', 'firstName', 'lastName', 'personID'],
                'Participates': ['eventID', 'personID'],
                'Event': ['eventID', 'type', 'audience', 'date', 'location'],
                'Orders': ['orderID', 'employeeID', 'fID'],
                'FutureItems': ['fID', 'title', 'author', 'type']
                }

# Helper function for createSchema, returns bool
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


# Initializes database by executing a series of CREATE TABLE statements
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

# Populated tables with example data using a series of INSERT INTO statements
def insertInto(conn):
    cur = conn.cursor()
    cur.execute('''
                INSERT OR IGNORE INTO Items(itemID, title, author, type, available)
                VALUES  ('1001', 'Love You Forever', 'Robert Munsch', 'Book', 1),
                        ('1002', 'The Paper Bag Princess', 'Robert Munsch', 'Book', 1),
                        ('1003', 'The Lightning Thief', 'Rick Riordan', 'Book', 1),
                        ('1004', 'Symphony in E Minor', 'Claude Debussy', 'CD', 1),
                        ('1005', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Online Book', 1),
                        ('1006', 'Rodrick Rules', 'Jeff Kinney', 'Comedy', 1),
                        ('1007', 'National Geographic', 'David Brindley', 'Magazine', 1),
                        ('1008', 'Geronimo Stilton: The Curse of the Cheese Pyramid', 'Geronimo Stilton', 'Adventure', 1),
                        ('1009', 'Pigs', 'Robert Munsch', 'Children', 1),
                        ('1010', 'Journal of Medicine', 'Brayden Sue', 'Scientific Journal', 1)
                ''')
    # print("Inserted items into Items")

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
    # print("Inserted records into Person")

    cur.execute('''
        INSERT OR IGNORE INTO Employee(employeeID, firstName, lastName, personID)
        VALUES  ('2001', 'John', 'Doe', '1001'),
                ('2002', 'Jane', 'Smith', '1002'),
                ('2003', 'Michael', 'Johnson', '1003'),
                ('2004', 'Emily', 'Williams', '1004'),
                ('2005', 'Daniel', 'Brown', '1005')
    ''')
    # print("Inserted records into Employee")

    cur.execute('''
        INSERT OR IGNORE INTO Event(eventID, type, audience, date, location)
        VALUES  ('2001', 'Book Launch', 'Children', '2023-07-31', 'Library Hall'),
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
    # print("Inserted records into Event")

    cur.execute('''
        INSERT OR IGNORE INTO FutureItems(fID, title, author, type)
        VALUES  ('3001', 'Lord of the Flies', 'William Golding', 'Book'),
                ('3002', 'The Plague', 'Albert Camus', 'Book'),
                ('3003', 'Tao Te Ching', 'Lao Tzu', 'Book'),
                ('3004', 'The Art of War', 'Sun Tzu', 'Book'),
                ('3005', 'The Pragmatic Programmer', 'Andrew Hunt, David Thomas', 'Book'),
                ('3006', 'Clean Code', 'Robert C. Martin', 'Book'),
                ('3007', 'Design Patterns', 'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides', 'Book'),
                ('3008', 'Introduction to Algorithms', 'Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein', 'Book'),
                ('3009', 'Artificial Intelligence: A Modern Approach', 'Stuart Russell, Peter Norvig', 'Book'),
                ('3010', 'Data Science from Scratch', 'Joel Grus', 'Book')
                ''')
    # print("Inserted records into FutureItems")
    conn.commit()

# Capitalizes each word in a space separated string to standardize before searching
def capitalizeWords(phraseString):
    wordList = phraseString.split(' ')
    wordListC = [word.capitalize() for word in wordList]
    result = ' '.join(wordListC)

    return result

"""
Returns a single record from Items
title, author: user inputs for search values
id (optional): returns the record with unique item id
"""
def searchItems(connection, title, author, id='-1'):
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

# Takes tuples from sqlite3 fetching and organizes into a pandas DataFrame before displaying
# records: list of tuples
# tableName: string name of table - used for dictionary lookup
def displayTable(records, tableName):
    try:
        table = pd.DataFrame(records, columns=dbAttributes[tableName])
        print("\n")
        topLine = "------------------------------------------------  " + tableName + "  ------------------------------------------------"
        print(topLine)
        print(table.to_string(index=False))
        print("\n")

    except:
        print("Error displaying data")


# Insert user inputted information into a record in Person
def makeAccount(connection):
    cur = connection.cursor()
    print("Please enter the following information.")
    firstName = input("First Name: ").capitalize()
    lastName = input("Last Name: ").capitalize()
    dob = input("Date of Birth (YYYY-MM-DD): ")
    # unique id calculated by max(id)+1
    cur.execute('SELECT MAX(personID) FROM Person;')
    maxID = cur.fetchone()[0]
    nextID = int(maxID) + 1 if maxID else 1000  # Starting from 1000 if no items exist yet

    try:
        sql = "INSERT INTO Person(" + ", ".join(dbAttributes['Person']) + ") "
        sql += "VALUES('" + str(nextID) + "', '" + firstName + "', '" + lastName + "', '" + dob + "');"

        cur.execute(sql)
        print("Account#:", str(nextID), "made successfully")
        connection.commit()
        return str(nextID)
    except:
        print("Error making account")
        return

# Find record from Person and add record in Employee, assigning a new employeeID
# returns True (success) or False (Failure)
def makeEmployee(connection, applicantID):
    cur = connection.cursor()

    # Check if employee record already exists for applicant
    cur.execute("SELECT employeeID FROM Employee WHERE personID = '" + applicantID + "';")
    existingEmployee = cur.fetchone()
    if existingEmployee:
        print("You have already been registered as an employee.")
        return

    # Generate unique employeeID
    cur.execute('SELECT MAX(employeeID) FROM Employee;')
    maxID = cur.fetchone()[0]
    nextID = int(maxID) + 1 if maxID else 1000  # Starting from 1000 if no items exist yet

    try:
        personRecord = findPersonID(connection, applicantID)
        print(personRecord)
        # If the record exists in Person, take the same personID, firstName, and lastName values
        if personRecord:
            personID = personRecord[0]
            firstName = personRecord[1]
            lastName = personRecord[2]
            sql = "INSERT INTO Employee(" + ", ".join(dbAttributes['Employee']) \
                  + ") VALUES('" + str(nextID) + "', '" + firstName + "', '" + lastName + "', '" + personID + "');"
            cur.execute(sql)
            print("Employee record for", firstName, lastName, "successfully created.")
            connection.commit()
            return True
        else:
            print("No record in Person table - please create an account first.")
            return False
    except:
        print("Error in employee creation system")

# Query Person table for given personID
# If found, returns record for that personID
def findPersonID(connection, personID):
    cur = connection.cursor()
    sql = "SELECT * FROM Person WHERE personID = '" + personID + "';"
    cur.execute(sql)
    result = cur.fetchone()
    if not result:
        choice = input("""ID not found, would you like to
        (1) Register for an account
        (2) Restart
        (Any Other Key) Exit
        """)
        if choice == '1':
            nextID = makeAccount(connection)
            findPersonID(connection, nextID)
        elif choice == '2':
            findPersonID(connection, input("ID: "))
        else:
            print("Exiting.")
            return False
    else:
        print("ID: " + result[0] + " found.")
        return result


def borrowItem(connection, personID, itemID):
    borrowDate = datetime.today()
    dateDue = (borrowDate + timedelta(days=30)).strftime('%Y-%m-%d')
    borrowDate = borrowDate.strftime('%Y-%m-%d')
    itemRecords = searchItems(connection, '', '', itemID)
    if itemRecords[0][4] == 0:
        print("No copies of " + itemRecords[0][1] + " currently available.")
        return

    try:
        sql = "INSERT INTO Borrows(" + ", ".join(dbAttributes['Borrows'][1:]) + ") "
        sql += "VALUES('" + personID + "', '" + itemID + "', '" + borrowDate + "', '" + dateDue + "', NULL, 0);"
        cur = connection.cursor()
        cur.execute(sql)
        print("Item borrowed successfully\n")
        cur.execute("UPDATE Items SET available = 0 WHERE itemID = '" + itemID + "';")
        connection.commit()
        return dateDue
    except:
        print("Error borrowing item\n")
        return


def returnItem(connection, personID):
    cur = connection.cursor()
    if findPersonID(connection, personID):
        sql = "SELECT * FROM Borrows WHERE personID = '" + personID + "';"
        cur.execute(sql)
        results = cur.fetchall()
        if not results:
            print("No items currently borrowed.")
            return False
        else:
            print("Your Borrowed Items:\n")
            displayTable(results, 'Borrows')
            returnID = input("ID of record you would like to return: ")
            sqlSelect = "SELECT * FROM Borrows WHERE borrowID = '" + returnID + "';"
            cur.execute(sqlSelect)
            resultFinal = cur.fetchone()
            if resultFinal:
                sqlDrop = "DELETE FROM Borrows WHERE personID = '" + personID + "' AND borrowID = '" + returnID + "';"
                cur.execute(sqlDrop)
                cur.execute("UPDATE Items SET available = 1 WHERE itemID = '" + str(resultFinal[2]) + "';")
                connection.commit()
                print("Item returned successfully.")
                return True
            else:
                print("Invalid selection")
                return False
    else:
        print("ID could not be determined.")


def donateItem(connection):
    cur = connection.cursor()

    # Get the maximum existing itemID from the database
    cur.execute('SELECT MAX(itemID) FROM Items')
    max_item_id = cur.fetchone()[0]

    # Increment it by 1 to get the next available itemID
    next_item_id = int(max_item_id) + 1 if max_item_id else 1000  # Starting from 1000 if no items exist yet

    title = capitalizeWords(input("Enter title: ").strip())
    author = capitalizeWords(input("Enter author: ").strip())
    item_type = capitalizeWords(input("Enter type: ").strip())

    try:
        # Insert the item data into the Items table
        cur.execute('''
            INSERT INTO Items(itemID, title, author, type, available)
            VALUES (?, ?, ?, ?, 1)
        ''', (str(next_item_id), title, author, item_type))
        connection.commit()
        print("Item donated successfully.")
    except sqlite3.Error as e:
        print("Error donating item:", e)
        connection.rollback()


def participateInEvent(connection):
    try:
        # Query all events
        sql = "SELECT * FROM Event;"
        cur = connection.cursor()
        cur.execute(sql)
        events = cur.fetchall()

        # Display the events
        displayTable(events, 'Event')

        event_id = input("Enter the eventID of the event you want to participate in: ")
        # Check if the event ID is valid
        valid_event_ids = [event[0] for event in events]

        if event_id not in valid_event_ids:
            print("Invalid eventID. Please try again.")
            return

        userID = input("Please enter your account ID: ")
        # Check if the userID is valid
        sql_person = "SELECT * FROM Person WHERE personID = ?;"
        cur.execute(sql_person, (userID,))
        person = cur.fetchone()

        if person is None:
            print("Invalid userID. The provided account ID does not exist. Please try again.")
            return

        # Ask the user to confirm participation
        confirm_participation = input("Do you want to participate in this event? (y/n): ")

        if confirm_participation.lower() == 'y':
            # Insert the participation record into the Participates table
            sql_insert_participation = "INSERT INTO Participates (eventID, personID) VALUES (?, ?);"
            cur.execute(sql_insert_participation, (event_id, userID))
            connection.commit()
            print("You have successfully registered for the event.")
        else:
            print("Registration canceled.")

    except Exception as e:
        print("Error occurred:", e)

# Find random employee to give assistance, outputs message
def requestHelp(connection):
    cur = connection.cursor()

    # Get the count of employees in the database
    cur.execute('SELECT COUNT(*) FROM Employee')
    num_employees = cur.fetchone()[0]

    if num_employees == 0:
        print("No employees available to assist at the moment.")
    else:
        # Get a random employee from the database
        random_employee_id = random.randint(2001, 2000 + num_employees)
        cur.execute('SELECT firstName FROM Employee WHERE employeeID = ?', (str(random_employee_id),))
        employee = cur.fetchone()

        if employee:
            first_name = employee[0]
            print(f"{first_name} is on their way to assist you! Please wait a moment...")
        else:
            print("No employees available to assist at the moment.")