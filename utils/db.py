import sqlite3
# Initialize the user dictionary database
conn_dict = sqlite3.connect('user_dictionary.db')
cursor_dict = conn_dict.cursor()
cursor_dict.execute('''
CREATE TABLE IF NOT EXISTS user_dictionary (
    user_id INTEGER,
    original TEXT,
    translation TEXT,
    language TEXT
)
''')
conn_dict.commit()

# Initialize the users database
conn_users = sqlite3.connect('users.db')
cursor_users = conn_users.cursor()
cursor_users.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    chat_id INTEGER UNIQUE,
    registration_date TEXT
)
''')
conn_users.commit()