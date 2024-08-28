import sqlite3

def init_db():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, service TEXT, username TEXT, url TEXT, 
                       password BLOB, notes TEXT)''')
    conn.commit()
    conn.close()

def add_password(service, username, url, password, notes):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, url, password, notes) VALUES (?, ?, ?, ?, ?)",
                   (service, username, url, password, notes))
    conn.commit()
    conn.close()

def get_password(service):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, url, password, notes FROM passwords WHERE service = ?", (service,))
    result = cursor.fetchone()
    conn.close()
    return result

def delete_password(service):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE service = ?", (service,))
    conn.commit()
    conn.close()

def backup_database():
    conn = sqlite3.connect('password_manager.db')
    with open('password_manager_backup.db', 'wb') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n'.encode('utf-8'))
    conn.close()

def restore_database():
    conn = sqlite3.connect('password_manager.db')
    with open('password_manager_backup.db', 'r') as f:
        conn.executescript(f.read())
    conn.close()
