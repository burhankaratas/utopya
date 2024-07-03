from flask import render_template, request, flash, redirect, url_for, session, Blueprint, current_app

from app.models.author_models import login_model
from app.utils.logs import save_http_request
from app.utils.functions import login_required

auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        userName = request.form.get("username")
        password = request.form.get("password")

        status, message = login_model(current_app.mysql, userName, password)

        if not status:
            flash(message, "danger")
            return redirect(url_for("auth.login"))

        else:
            data = message

            session['logged_in'] = True
            session['id'] = data['id']
            session['userName'] = data['userName']
            session['email'] = data['email']
            session['IsAdmin'] = data['IsAdmin']
            session['IsVerified'] = data['IsVerified']
            session['profileImage'] = data['profileImage']

            if data['IsVerified'] == 0:
                return redirect(url_for("editprofile"))
            else:
                return redirect(url_for("main.index"))
            

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
            

@auth.before_request
def log_request_info():
    save_http_request()