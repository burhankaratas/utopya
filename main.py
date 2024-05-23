from flask import render_template
import os

from config import create_app, init_mysql

app = create_app()
mysql = init_mysql(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50))
    app.run(host="0.0.0.0", port=port, debug=True)