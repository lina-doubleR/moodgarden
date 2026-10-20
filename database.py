import sqlite3
from fpdf import FPDF
from datetime import date
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

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

def get_moods_dict():
    all_moods = get_all_moods()
    moods_by_date = {}
    for entry in all_moods:
        moods_by_date[entry[2]] = entry[1]
    return moods_by_date

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

    pdf.set_font("DejaVu", size=20)
    pdf.set_text_color(214, 51, 108)
    pdf.cell(0, 15, "Mood Garden", ln=True, align="C")

    pdf.set_font("DejaVu", size=12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Дневник настроений", ln=True, align="C")
    pdf.ln(10)

    for entry in moods:
        if entry[1] == "ромашечка":
            pdf.set_text_color(217, 119, 6)
        elif entry[1] == "розочка":
            pdf.set_text_color(214, 51, 108)
        else:
            pdf.set_text_color(107, 114, 128)

        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 8, f"{entry[2]} — {entry[1]}", ln=True)

        if entry[3]:
            pdf.set_text_color(130, 130, 130)
            pdf.set_font("DejaVu", size=10)
            pdf.cell(0, 6, entry[3], ln=True)

        pdf.ln(3)

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

def create_chart():
    stats = get_mood_stats()

    names = [row[0] for row in stats]
    counts = [row[1] for row in stats]

    plt.figure()
    plt.bar(names, counts, color=["#fbbf24", "#f472b6", "#9ca3af"])
    plt.title("Настроения")
    plt.ylabel("Количество раз")
    plt.savefig("static/chart.png")
    plt.close()