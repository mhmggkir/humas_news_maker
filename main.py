import webbrowser, json, threading, time
from flask import Flask, render_template, request
from flask_cors import CORS
from news_generator import make_news

app = Flask(__name__)
CORS(app)

news_url_list = []

with open("config.json") as j:
  data = json.load(j)
  port = data["port"]

def on_ready():
  time.sleep(0.5)
  webbrowser.open(f"http://localhost:{port}")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
  if request.method == "POST":
    make_news(request.json["URLList"])
  return "News generated"

def main():
  threading.Thread(target=on_ready).start()
  app.run("127.0.0.1", port)

main()
