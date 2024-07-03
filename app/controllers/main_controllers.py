from app.utils.logs import save_http_request
from app.models.main_models import index_model, yazarlar_model, yazi_model, profile_model

from flask import Blueprint, session, redirect, url_for, render_template, current_app, flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if "logged_in" in session:
        if session["IsVerified"] == 1:
            return redirect(url_for("post.blogindex"))
        
    status, message = index_model(current_app.mysql)

    if not status:
        flash(message, "danger")
        return redirect(url_for("main.index"))
    
    else:
        datas = message

        if datas is None:
            flash("Gösterilecek yazı bulunamadı.", "warning")
            datas = []

        return render_template("index.html", datas = datas)


@main.route('/hakkimizda')
def about():
    return render_template("hakkimizda.html")

@main.route("/yazarlar")
def yazarlar():
    status, message = yazarlar_model(current_app.mysql)

    if not status:
        flash(message, "danger")
        return redirect(url_for("main.yazarlar"))
    
    else:
        datas = message

        if datas is None:
            flash("Herhangi bir yazar hesabı bulunmamakta", "warning")
            datas = []

        return render_template("yazarlar.html", datas = datas)
        
@main.route("/p/<url>")
def yazi(url):
    status, message, profileImage, user = yazi_model(current_app.mysql, url)

    if not status:
        flash(message, "danger")
        return redirect(url_for("main.yazi", url=url))
    
    else:
        data = message

        if profileImage == None:
            print("şuan buradasınız")
            return render_template("yazi.html", data=data)
        
        else:
            print("burada değilsin")
            print(profileImage)
            return render_template("yazi.html", data=data, profileImage = profileImage, user = user)
        
@main.route("/@<userName>")
def profile(userName):
    status, message, gonderidatas = profile_model(current_app.mysql, userName)

    if not status:
        flash(message, "danger")
        return redirect(url_for("main.index"))
    
    else:
        data = message
        return render_template("profile.html", data=data, userName=userName, gonderidatas = gonderidatas)

@main.before_request
def log_request_info():
    save_http_request()