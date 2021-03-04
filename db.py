import sqlite3

conn = sqlite3.connect("pos.sqlite")

cursor = conn.cursor()
users_query = """ CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY,
    username text NOT NULL,
    role text NOT NULL,
    password text NOT NULL
)"""

cursor.execute(users_query)
cursor = conn.cursor()
inv_query = """ CREATE TABLE IF NOT EXISTS inventory (
    pid integer PRIMARY KEY,
    product text NOT NULL,
    price integer NOT NULL,
    quantity integer NOT NULL
)"""

cursor.execute(inv_query)

cursor = conn.cursor()
busket_query = """ CREATE TABLE IF NOT EXISTS busket (
    pid integer PRIMARY KEY,
    product text NOT NULL,
    price integer NOT NULL,
    quantity integer NOT NULL
)"""

cursor.execute(busket_query)