from flask import Flask, render_template, request
from database import init_db, add_mood
from datetime import date
from database import init_db, add_mood, get_all_moods
from database import init_db, add_mood, get_all_moods, get_mood_stats
from database import init_db, add_mood, get_all_moods, get_mood_stats, get_recent_moods
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    recent = get_recent_moods()
    return render_template("home.html", recent_moods=recent)


@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        selected_mood = request.form.get("mood")
        today = str(date.today())
        add_mood(selected_mood, today)
    return render_template("mood.html")

@app.route("/history")
def history():
    all_moods = get_all_moods()
    return render_template("history.html", moods=all_moods)

@app.route("/stats")
def stats():
    mood_stats = get_mood_stats()
    return render_template("stats.html", stats=mood_stats)

@app.route("/set_theme/<theme_name>")
def set_theme(theme_name):
    response = make_response(redirect(url_for("home")))
    response.set_cookie("theme", theme_name)
    return response

@app.context_processor
def inject_theme():
    theme = request.cookies.get("theme", "pink")
    return dict(theme=theme)

if __name__ == "__main__":
    app.run(debug=True)

