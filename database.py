import sqlite3
from fpdf import FPDF
from datetime import date

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

def add_mood(mood, date, note):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO moods (mood, date, note) VALUES (?, ?, ?)", (mood, date, note))
    connection.commit()
    connection.close()

def get_all_moods():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM moods ORDER BY id DESC")
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_mood_stats():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT mood, COUNT(*) FROM moods GROUP BY mood")
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_recent_moods(limit=7):
    all_moods = get_all_moods()
    return all_moods[:limit]

def create_pdf():
    moods = get_all_moods()

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf")
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, "Mood Garden - дневник настроений", ln=True)
    pdf.ln(5)

    pdf.set_font("DejaVu", size=11)
    for entry in moods:
        line = f"{entry[2]} - {entry[1]}"
        pdf.cell(0, 8, line, ln=True)

    pdf.output("history.pdf")

def mood_logged_today():
    today = str(date.today())
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM moods WHERE date = ?", (today,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def delete_mood(mood_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM moods WHERE id = ?", (mood_id,))
    connection.commit()
    connection.close()