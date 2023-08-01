import sqlite3
import library

library.createSchema()


conn = sqlite3.connect('library.db')
print("Connection to library.db successful")
cursor = conn.cursor()
library.insertInto(conn)

done = False

while not done:
    choice = input('''
    Welcome to the library database, what would you like to do?
    (1) Find an item
    (2) Return an item
    (3) Donate an item
    (4) Find an event
    (5) Volunteer for the library
    (6) Request help from librarian
    (x) Exit
    ''')

    if choice == '1':

        print("Here is a list of all of the books that we have in our catalogue! Feel free to look around.")
        cursor.execute("SELECT * FROM Items")
        rows = cursor.fetchall()
        library.displayTable(rows, "Items")
        print("If you want to borrow a book, just fill in the form below and you are good to go!")

        #list of all itemids
        cursor.execute('SELECT itemID FROM Items')
        itemIDs = [row[0] for row in cursor.fetchall()]

        title = library.capitalizeWords(input("Title: ").strip())
        author = library.capitalizeWords(input("Author: ").strip())
        results = library.searchItems(conn, title, author)
        if len(results) > 0:
            selectID = input("borrowID of required item (x to cancel): ")
            if selectID == 'x':
                continue
            if selectID not in (itemIDs):
                print("Invalid itemID. Please enter a correct itemID.")
                continue
            results = library.searchItems(conn, title, author, selectID)
            choice = ''
            while choice not in ['Y', 'N']:
                choice = input("Borrow this book (y/n)?: ").upper()
                if choice == 'Y':
                    personID = input("Please enter your ID: ")
                    if library.findPersonID(conn, personID):
                        dateDue = library.borrowItem(conn, personID, results[0][0])
                        if dateDue:
                            print("Please return by " + dateDue)
                    else:
                        choice = 'retry'

                elif choice == 'N':
                    continue
                else:
                    print("Please enter Y (yes) or N (no).")
        else:
            print("No items found matching your search :(")

    elif choice == '2':

        userID = input("Please enter your ID: ")
        library.returnItem(conn, userID)

    elif choice == '3':
        # input values of item, form into tuple
        library.donateItem(conn)

    elif choice == '4':
        library.participateInEvent(conn)
        # query all events
        # input to pick one
        # input y/n to register
        # if y: insert into participates
    elif choice == '5':
        volunteerID = ''
        while volunteerID != 'done':
            volunteerID = input("What is your ID? (x to cancel): ").strip()
            if volunteerID == 'x':
                volunteerID = 'done'
            elif library.findPersonID(conn, volunteerID):
                confirm = ''
                while confirm not in ['Y', 'N']:
                    confirm = input("ID found, make employee record (y/n)?: ").upper().strip()
                    if confirm == 'Y':
                        library.makeEmployee(conn, volunteerID)
                        print("Employee record created.")
                        volunteerID = 'done'
                    elif confirm == 'N':
                        continue
                    else:
                        print("Please enter Y (yes) or N (no).")
            else:
                print("Please re-enter ID")
    #
    elif choice == '6':
        library.requestHelp(conn)

    elif choice == 'x':
        print("Exiting application.")
        done = True

    else:
        print("Invalid selection")

conn.close()
