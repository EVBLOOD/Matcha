from flask import Flask
from app.core.database import Database

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"