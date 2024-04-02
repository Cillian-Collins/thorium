import sqlite3


def insert_submission(flag, status, target, script):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO submissions (flag, status, target, script, service) VALUES (?, ?, ?, ?, (SELECT service "
        "FROM exploits WHERE name = ?))",
        (flag, status, target, script, script),
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_submissions(submissions):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()

    data = [[submission[0], submission[1], submission[2], submission[3], submission[3]] for submission in submissions]
    cursor.executemany(
        "INSERT INTO submissions (flag, status, target, script, service) VALUES (?, ?, ?, ?, (SELECT service FROM exploits WHERE name = ?))",
        data
    )
    conn.commit()
    cursor.close()
    conn.close()