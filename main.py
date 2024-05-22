from flask import Flask, render_template
import os

from config import create_app

app = create_app()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50))
    app.run(host="0.0.0.0", port=port, debug=True)