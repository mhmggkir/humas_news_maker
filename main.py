print("hello World!!")

from flask import Flask, render_template, request
from flask_cors import CORS
from news_generator import make_news
import threading
import socket
import time
import webbrowser

app = Flask(__name__)
CORS(app)

news_url_list = []

def is_port_used(port):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      return s.connect_ex(("localhost", port)) != 0

def on_ready():
  while is_port_used(5000):
     time.sleep(0.1)
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
  threading.Thread(target=on_ready).start()
  if(not is_port_used(5000)):
    app.run("127.0.0.1", 5000)

if __name__ == "__main__":
   main()
