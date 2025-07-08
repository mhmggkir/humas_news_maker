from flask import Flask, render_template, request
from flask_cors import CORS
from news_generator import make_news
import time
import webbrowser

app = Flask(__name__)
CORS(app)

news_url_list = []

def on_ready():
  time.sleep(1)
  webbrowser.open_new("http://localhost:5000")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
  if request.method == "POST":
    make_news(request.json["URLList"])
  return "News generated"

def main():
  on_ready()
  app.run("127.0.0.1", 5000, debug=True)

if __name__ == "__main__":
   main()
