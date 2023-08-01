import sqlite3
import library

library.createSchema()

conn = sqlite3.connect('library.db')
print("Connection to library.db successful")
cursor = conn.cursor()

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
        title = library.capitalizeWords(input("Title: "))
        author = library.capitalizeWords(input("Author: "))
        results = library.searchItems(conn, title, author)
        if len(results) > 1:
            selectID = input("ID of required item: ")
            results = library.searchItems(conn, title, author, selectID)
            choice = ''
            while choice not in ['Y', 'N']:
                choice = input("Borrow this book (y/n)?").upper()
                if choice == 'Y':
                    personID = input("Please enter your ID: ")
                    if library.findPersonID(conn, personID):
                        dateDue = library.borrowBook(conn, personID, results[0][0])
                        if dateDue:
                            print("Please return by " + dateDue)
                        else:
                            choice = 'retry'

                elif choice == 'N':
                    continue
                else:
                    print("Please enter Y (yes) or N (no).")

    elif choice == '2':

        userID = input("Please enter your ID: ")
        library.returnItem(conn, userID)

    elif choice == '3':
        pass
        # input values of item, form into tuple
        # insert into items
    elif choice == '4':
        pass
        # query all events
        # input to pick one
        # input y/n to register
        # if y: insert into participates
    elif choice == '5':
        pass
        # find record in people, if not there insert record
        # insert record from people into employee
    elif choice == '6':
        pass
        # query employees, input to pick one
        # print(name, "is on their way!")

    elif choice == 'x':
        print("Exiting application.")
        done = True

    else:
        print("Invalid selection")

conn.close()