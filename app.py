from flask import Flask, render_template
from waitress import serve
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")
  
if __name__ == "__main__":
    logging.info("Starting server...")
    serve(app)

