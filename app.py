from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        selected_mood = request.form.get("mood")
        print(selected_mood)
    return render_template("mood.html")

if __name__ == "__main__":
    app.run(debug=True)