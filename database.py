import sqlite3


def get_connection():
    connection = sqlite3.connect("moodgarden.db")
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def add_mood(mood, date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO moods (mood, date) VALUES (?, ?)", (mood, date))
    connection.commit()
    connection.close()