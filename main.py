import sqlite3
import library

conn = sqlite3.connect('library.db')
print("Connection to library.db successful")
cursor = conn.cursor()

done = False

while not done:
    choice = input('''
    Welcome to the library database, what would you like to do?\
    (1) Find an item
    (2) Return an item
    (3) Donate an item
    (4) Find an event
    (5) Volunteer for the library
    (6) Request help from librarian
    (x) Exit
    ''')

    if choice == '1':
        # input for title, author
        # results = query
        # print(results)
        # if len(results) > 1:
            # id = input("id of requested item")
            # query for id
            # assert len(result) == 1
            # choice = input("borrow", result[0].title) y/n
            # if y:
            #   insert into borrows
    elif choice == '2':
        # input for book in borrows table
        # results = query
        # if len(results) == 1
        # input y/n to return book
        # if y: update items, delete from borrows
    elif choice == '3':
        # input values of item, form into tuple
        # insert into items
    elif choice == '4':
        # query all events
        # input to pick one
        # input y/n to register
        # if y: insert into participates
    elif choice == '5':
        # find record in people, if not there insert record
        # insert record from people into employee
    elif choice == '6':
        # query employees, input to pick one
        # print(name, "is on their way!")

    elif choice == 'x':
        done = True

    else:
        print("Invalid selection")


sql = "CREATE TABLE Items(itemID);"
library.createTable(conn, )
conn.close()