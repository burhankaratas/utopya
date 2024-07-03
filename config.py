from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

def config_app(app):
    UPLOAD_FOLDER = '/app/static/uploads'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    app.secret_key = os.getenv("SECRET_KEY")

    return app

def init_mysql(app):
    mysql = MySQL(app)
    return mysql