import sqlite3

def init_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # Create tables for emails
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails 
                      (id TEXT PRIMARY KEY, sender TEXT, subject TEXT, 
                       body TEXT, date TEXT, seen INTEGER)''')
    conn.commit()
    conn.close()

def insert_email(path, uid, sender, subject, body, date, seen):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # "INSERT OR IGNORE" prevents duplicates if you sync the same email twice
    cursor.execute('''
        INSERT OR IGNORE INTO emails (id, sender, subject, body, date, seen)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (uid, sender, subject, body, date, seen))
    conn.commit()
    conn.close()