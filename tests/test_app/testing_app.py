from flask import Flask
import os
from logging.config import dictConfig
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)
db = SQLAlchemy(app)

from .urls import *

if __name__ == "__main__":
    app.run()
