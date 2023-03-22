import threading
from flask import Flask, render_template
from waitress import serve
from limitcoins import limit_coins

app = Flask(__name__)

# updates data every 2 minutes
def update_data(func):
    def wrapper():
        update_data(func)
        func()
    t = threading.Timer(120, wrapper)
    t.start()
    return

try:
   limit_coins()
   update_data(limit_coins)
except Exception as e:
   print(e)
   print("failed to update")


@app.route("/")
def index():
  return render_template("app.html")

if __name__ == "__main__":
  app.run('0.0.0.0',port=8081)
#   serve(app)

