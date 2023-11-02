import sqlite3


def insert_submission(flag, status, target, script):
    # Create a new database connection for this thread
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO submissions (flag, status, target, script, service) VALUES (?, ?, ?, ?, (SELECT service "
        "FROM exploits WHERE name = ?))",
        (flag, status, target, script, script),
    )
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()

    return items
