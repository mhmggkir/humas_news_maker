import webbrowser, json, threading, time, os
from flask import Flask, render_template, request
from flask_cors import CORS
from news_generator import make_news

if not os.path.exists(".env") or not os.path.exists("config.json"):
  print(".env or config.json file isn't exist")
  exit()

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
