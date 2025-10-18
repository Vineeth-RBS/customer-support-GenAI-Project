from flask import Flask
from dotenv import load_dotenv
import os
from models import Base, get_engine_and_session

load_dotenv()
app = Flask(__name__)

# ---- Database setup ---- #
engine, Session = get_engine_and_session()
Base.metadata.create_all(bind=engine)   # Create tables if not exist

@app.route("/")
def home():
    return "Database initialized ✅"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
