from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Привет! Это Mood Garden 🌸"


if __name__ == "__main__":
    app.run(debug=True)