import sqlite3


def insert_submission(flag, status, target, script):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO submissions (flag, status, target, script, service) VALUES (?, ?, ?, ?, (SELECT service "
        "FROM exploits WHERE name = ?))",
        (flag, status, target, script, script),
    )
    items = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return items
