import os
import sqlite3


def setup_database():
    database_file = '/database/database.db'

    if not os.path.exists(database_file):
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS exploits (id INTEGER PRIMARY KEY, name TEXT, active BOOLEAN, service INT)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY, flag TEXT, status TEXT CHECK( status IN '
            '("OK", "OLD", "DUP", "INV", "OWN", "ERR") ) , script TEXT, service INT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, name TEXT, port INT CHECK(port '
                       '>= 0 AND port <= 65535))')

        # Insert a sample row into the "submissions" tables
        cursor.execute('INSERT INTO submissions (flag, status, script, service) VALUES (?, ?, ?, ?)', (
            "ECSC_ZQUMGjrRAK4BKBdnd8Il9wEVGvcG",
            "OK",
            "exploit.py",
            "1"
        ))

        conn.commit()  # Commit the changes to the database
        conn.close()

    # If the database file already exists, just connect to it
    conn = sqlite3.connect(database_file)
    return conn


def fetch_exploits():
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, (SELECT name FROM services WHERE id = service), active FROM exploits")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def fetch_exploit_by_id(exploit_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, (SELECT name FROM services WHERE id = service), active FROM exploits WHERE id = ?", (exploit_id,))
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def fetch_exploits_by_service(service_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exploits WHERE service = ?", (service_id,))
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def fetch_services():
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def fetch_exploit_name_by_id(exploit_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM exploits WHERE id = ?", (exploit_id,))
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    if len(items) == 0 or len(items[0]) == 0:
        return None

    return items[0][0]


def fetch_submissions():
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, flag, status, script, (SELECT name FROM services WHERE id = service) FROM submissions")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def insert_exploit(name, service, active):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO exploits (name, service, active) VALUES (?, ?, ?)', (name, service, active))

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()


def insert_service(name, port):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO services (name, port) VALUES (?, ?)', (name, port))

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()


def remove_service(service_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM services WHERE id = ?', (service_id,))

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()


def disable_exploit(exploit_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE exploits SET active = NOT active WHERE id = ?', (exploit_id,))

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()


def remove_exploit(exploit_id):
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM exploits WHERE id = ?', (exploit_id,))

    # Close the cursor and connection within this thread
    conn.commit()
    cursor.close()
    conn.close()


def fetch_exploits_breakdown():
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) AS active_true_count, SUM(CASE WHEN active = 0 "
                   "THEN 1 ELSE 0 END) AS active_false_count FROM exploits;")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items


def fetch_submissions_breakdown():
    # Create a new database connection for this thread
    conn = sqlite3.connect('/database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CASE WHEN status = 'OK' THEN 1 ELSE 0 END) AS OK, SUM(CASE WHEN status = 'OLD' THEN 1 "
                   "ELSE 0 END) AS OLD, SUM(CASE WHEN status = 'DUP' THEN 1 ELSE 0 END) AS DUP, SUM(CASE WHEN status "
                   "= 'INV' THEN 1 ELSE 0 END) AS INV, SUM(CASE WHEN status = 'OWN' THEN 1 ELSE 0 END) AS OWN, "
                   "SUM(CASE WHEN status = 'ERR' THEN 1 ELSE 0 END) AS ERR FROM submissions;")
    items = cursor.fetchall()

    # Close the cursor and connection within this thread
    cursor.close()
    conn.close()

    return items
