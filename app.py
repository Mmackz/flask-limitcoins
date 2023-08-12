from flask import Flask, render_template
from modules import authenticate, update
from waitress import serve
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

reddit = authenticate()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/update_data", methods=["POST"])
def update_data():
    try:
        update(reddit)
        logging.info('Data updated successfully')
        return "Data updated successfully"
    except Exception as e:
        logging.error(f"Error updating data: {str(e)}")
        return f"Error: {str(e)}", 500
  
if __name__ == "__main__":
    logging.info("Starting server...")
    serve(app)

