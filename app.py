from flask import Flask, render_template
from modules import authenticate, update
from waitress import serve

reddit = authenticate()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/update_data", methods=["POST"])
def update_data():
    update(reddit)
    return "Data updated successfully"
  
if __name__ == "__main__":
#   app.run("0.0.0.0",port=8081)
    serve(app)

