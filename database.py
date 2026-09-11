import sqlite3

DATABASE = "evidence.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        case_id TEXT,
        investigator TEXT,
        description TEXT,
        filename TEXT,
        file_hash TEXT,
        upload_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_evidence(case_id, investigator, description,
                 filename, file_hash, upload_time):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO evidence
    (case_id, investigator, description,
     filename, file_hash, upload_time)

    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        investigator,
        description,
        filename,
        file_hash,
        upload_time
    ))

    conn.commit()
    conn.close()


def get_all_evidence():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT case_id,
           investigator,
           description,
           filename,
           file_hash,
           upload_time
    FROM evidence
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def total_evidence():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM evidence")

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_hash(case_id, filename):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_hash
        FROM evidence
        WHERE case_id = ?
        AND filename = ?
        """,
        (case_id, filename)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def search_case(case_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT case_id,
               investigator,
               description,
               filename,
               file_hash,
               upload_time
        FROM evidence
        WHERE case_id = ?
    """, (case_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows