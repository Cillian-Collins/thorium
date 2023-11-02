import sqlite3


def fetch_active_exploits():
    # Create a new database connection for this thread
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM exploits WHERE active")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items
