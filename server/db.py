import sqlite3
import os


def setup_database():
    database_file = 'database.db'

    if not os.path.exists(database_file):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS exploits (id INTEGER PRIMARY KEY, name TEXT, active BOOLEAN)')

        # Insert a sample row into the "exploits" table
        cursor.execute('INSERT INTO exploits (name, active) VALUES (?, ?)', ("example.py", True))

        conn.commit()  # Commit the changes to the database
        conn.close()

    # If the database file already exists, just connect to it
    conn = sqlite3.connect(database_file)
    return conn


def fetch_exploits():
    # Create a new database connection for this thread
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items