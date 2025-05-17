import sqlite3

connaction = sqlite3.connect('database.db')
cursor = connaction.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT
)
''')
connaction.commit()

def insert_user(chat_id, first_name, last_name, username):
    cursor.execute('''
        INSERT OR REPLACE INTO users (chat_id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, first_name, last_name, username))
    connaction.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS bans (
    chat_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT
)
''')
connaction.commit()

def ban_user(chat_id, first_name, last_name, username):
    cursor.execute('''
        INSERT OR REPLACE INTO bans (chat_id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)
    ''', (chat_id, first_name, last_name, username))
    connaction.commit()

def unban_user(chat_id):
    cursor.execute('''
        DELETE FROM bans WHERE chat_id=?
    ''', (chat_id,))
    connaction.commit()

def is_user_banned(chat_id):
    cursor.execute('SELECT 1 FROM bans WHERE chat_id=?', (chat_id,))
    return cursor.fetchone() is not None
