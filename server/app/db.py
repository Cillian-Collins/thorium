import os
import sqlite3


def setup_database():
    database_file = "/database/database.db"

    if not os.path.exists(database_file):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS exploits (id INTEGER PRIMARY KEY, name TEXT, active BOOLEAN, service INT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY, flag TEXT, status TEXT CHECK( status IN "
            '("OK", "OLD", "DUP", "INV", "OWN", "ERR") ), target TEXT, script TEXT, service INT)'
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, name TEXT, port INT CHECK(port "
            ">= 0 AND port <= 65535))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS targets (id INTEGER PRIMARY KEY, host TEXT)"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS disabled (id INTEGER PRIMARY KEY, host TEXT, exploit_id TEXT)"
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect(database_file)
    return conn


def fetch_exploits():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, (SELECT name FROM services WHERE id = service), active FROM exploits"
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_exploit_by_id(exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, (SELECT name FROM services WHERE id = service), active FROM exploits WHERE id = ?",
        (exploit_id,),
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_exploits_by_service(service_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits WHERE service = ?", (service_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_services():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_exploit_name_by_id(exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM exploits WHERE id = ?", (exploit_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(items) == 0 or len(items[0]) == 0:
        return None

    return items[0][0]


def fetch_submissions():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, flag, status, target, script, (SELECT name FROM services WHERE id = service) FROM "
        "submissions"
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_paginated_submissions(page, per_page):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()

    offset = (page - 1) * per_page

    cursor.execute(
        "SELECT id, flag, status, target, script, (SELECT name FROM services WHERE id = service) FROM "
        "submissions ORDER BY id DESC LIMIT ? OFFSET ?",
        (per_page, offset),
    )
    items = cursor.fetchall()

    conn.close()
    return items


def insert_exploit(name, service, active):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO exploits (name, service, active) VALUES (?, ?, ?)",
        (name, service, active),
    )

    conn.commit()
    cursor.close()
    conn.close()


def insert_service(name, port):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (name, port) VALUES (?, ?)", (name, port))

    conn.commit()
    cursor.close()
    conn.close()


def remove_service(service_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))

    conn.commit()
    cursor.close()
    conn.close()


def disable_exploit(exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE exploits SET active = NOT active WHERE id = ?", (exploit_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()


def remove_exploit(exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exploits WHERE id = ?", (exploit_id,))

    conn.commit()
    cursor.close()
    conn.close()


def fetch_exploits_breakdown():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) AS active_true_count, SUM(CASE WHEN active = 0 "
        "THEN 1 ELSE 0 END) AS active_false_count FROM exploits;"
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def fetch_submissions_breakdown():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(CASE WHEN status = 'OK' THEN 1 ELSE 0 END) AS OK, SUM(CASE WHEN status = 'OLD' THEN 1 "
        "ELSE 0 END) AS OLD, SUM(CASE WHEN status = 'DUP' THEN 1 ELSE 0 END) AS DUP, SUM(CASE WHEN status "
        "= 'INV' THEN 1 ELSE 0 END) AS INV, SUM(CASE WHEN status = 'OWN' THEN 1 ELSE 0 END) AS OWN, "
        "SUM(CASE WHEN status = 'ERR' THEN 1 ELSE 0 END) AS ERR FROM submissions;"
    )
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def insert_targets(targets):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM targets")

    cursor.executemany("INSERT INTO targets (host) VALUES (?)", [(target,) for target in targets])

    conn.commit()
    cursor.close()
    conn.close()


def fetch_targets():
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM targets")
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items


def add_exploit_exclusions(hosts, exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    print(hosts, exploit_id)
    cursor.executemany("INSERT INTO disabled (host, exploit_id) VALUES (?, ?)", [(host, exploit_id) for host in hosts])
    conn.commit()
    cursor.close()
    conn.close()

def remove_exploit_exclusions(hosts, exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.executemany("DELETE FROM disabled WHERE host = ? AND exploit_id = ?", [(host, exploit_id) for host in hosts])
    conn.commit()
    cursor.close()
    conn.close()


def fetch_disabled_exploits(exploit_id):
    conn = sqlite3.connect("/database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT host, exploit_id FROM disabled WHERE exploit_id = ?", (exploit_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return items