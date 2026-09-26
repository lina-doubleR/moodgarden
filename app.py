from flask import Flask, render_template, request
from database import init_db, add_mood
from datetime import date

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        selected_mood = request.form.get("mood")
        today = str(date.today())
        add_mood(selected_mood, today)
    return render_template("mood.html")


if __name__ == "__main__":
    app.run(debug=True)