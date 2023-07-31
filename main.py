import sqlite3
import library

conn = sqlite3.connect('library.db')
print("Connected to library.db")
cursor = conn.cursor()

sql = "CREATE TABLE Items(itemID);"
library.createTable(conn, )
conn.close()