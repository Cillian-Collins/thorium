import sqlite3


def fetch_active_exploits():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM exploits WHERE active")
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_targets():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host FROM targets")
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items
