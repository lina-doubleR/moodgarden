from datetime import date
import calendar
from database import init_db, add_mood, get_all_moods, get_mood_stats, get_recent_moods, create_pdf, mood_logged_today, delete_mood, create_chart, get_moods_dict
from flask import Flask, render_template, request, redirect, url_for, make_response, send_file

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    recent = get_recent_moods()
    logged_today = mood_logged_today()
    return render_template("home.html", recent_moods=recent, logged_today=logged_today)


@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        selected_mood = request.form.get("mood")
        note = request.form.get("note")
        today = str(date.today())
        add_mood(selected_mood, today, note)
    return render_template("mood.html")

@app.route("/history")
def history():
    all_moods = get_all_moods()
    return render_template("history.html", moods=all_moods)

@app.route("/stats")
def stats():
    mood_stats = get_mood_stats()
    create_chart()
    return render_template("stats.html", stats=mood_stats)

@app.route("/set_theme/<theme_name>")
def set_theme(theme_name):
    response = make_response(redirect(url_for("home")))
    response.set_cookie("theme", theme_name)
    return response

@app.route("/download_pdf")
def download_pdf():
    create_pdf()
    return send_file("history.pdf", as_attachment=True)

@app.route("/delete/<int:mood_id>")
def delete(mood_id):
    delete_mood(mood_id)
    return redirect(url_for("history"))

@app.route("/calendar")
def calendar_view():
    today = date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)

    grid = []
    for week in weeks:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                day_date = date(year, month, day)
                week_data.append((day, str(day_date)))
        grid.append(week_data)

    moods_by_date = get_moods_dict()
    month_name = calendar.month_name[month]

    return render_template("calendar.html", grid=grid, moods_by_date=moods_by_date, month_name=month_name, year=year)

@app.context_processor
def inject_theme():
    theme = request.cookies.get("theme", "pink")
    return dict(theme=theme)

if __name__ == "__main__":
    app.run(debug=True)

# лялялялялля