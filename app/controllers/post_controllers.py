from app.utils.logs import save_http_request
from app.utils.functions import login_required, date, generate_url, admin_required

from app.models.post_models import yazilar_model, yaziekle_model, taslaklar_model, gonderi_guncelle_get_model, gonderi_guncelle_post_model, yazisil_model, taslak_model, pubrequest_model, onaybekleyenler_model, publishwait_model

from flask import Blueprint, session, current_app, flash, redirect, url_for, render_template, request

post = Blueprint('post', __name__)

@post.route("/index")
@login_required
def blogindex():
    return render_template("blogindex.html")


@post.route('/yazilarim')
@login_required
def yazilar():
    status, message = yazilar_model(current_app.mysql)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.yazilar"))
    
    else:
        datas = message

        return render_template("yazilarim.html", datas = datas)
    
@post.route("/yazi-yaz", methods = ["GET", "POST"])
@login_required
def yaziekle():
    if request.method == "GET":
        return render_template("yaziyaz.html")
    
    elif request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        hastag = request.form.get("hastag")

        blogContent = request.form.get("blogContent")

        writer = session["userName"]
        createdDate = date()
        url = generate_url(title)

        status, message = yaziekle_model(current_app.mysql, title, content, blogContent, writer, createdDate, url, hastag)

        if not status:
            flash(message, "danger")
            return redirect(url_for("post.yaziekle"))

        else:
            flash(message, "success")
            return redirect(url_for("post.yazilar"))
        
@post.route("/taslaklar")
@login_required
def taslaklar():
    status, message = taslaklar_model(current_app.mysql)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.yazilar"))
    
    else:
        datas = message

        return render_template("taslaklar.html", datas = datas)
    
@post.route("/gonderi-guncelle/<id>", methods = ["GET", "POST"])
@login_required
def gonderiguncelle(id):
    if request.method == "GET":
        status, message = gonderi_guncelle_get_model(current_app.mysql, id)

        if not status:
            flash(message, "danger")
            return redirect(url_for("post.yazilar"))
        
        else:
            data = message

            return render_template("gonderiguncelle.html", data = data)
        
    elif request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        blogContent = request.form.get('blogContent')
        hastag = request.form.get('hastag')

        status, message = gonderi_guncelle_post_model(current_app.mysql, title, content, blogContent, hastag, id)

        if not status:
            flash(message, "danger")
            return redirect(url_for("post.yazilar"))
        
        else:
            flash(message, "success")
            return redirect(url_for("post.yazilar"))
        
@post.route("/delete/<id>")
@login_required
def yazisil(id):
    status, message = yazisil_model(current_app.mysql, id)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.yazilar"))
    
    else:
        flash(message, "success")
        return redirect(url_for("post.yazilar"))

@post.route("/taslak/<id>")
def taslak(id):
    status, message = taslak_model(current_app.mysql, id)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.taslaklar"))
    
    else:
        data = message

        return render_template("yazi.html", data = data)
    
@post.route("/pub/<id>")
def pubrequest(id):
    status, message = pubrequest_model(current_app.mysql, id)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.taslaklar"))

    else:
        flash(message, "success")
        return redirect(url_for("post.taslaklar"))
    
@post.route("/onay-bekleyenler")
@admin_required
def onaybekleyenler():
    status, message = onaybekleyenler_model(current_app.mysql)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.blogindex"))
    
    else:
        datas = message

        return render_template("onaybekleyenler.html", datas = datas)
    
@post.route("/publish/<id>")
@admin_required
def publishwait(id):
    status, message = publishwait_model(current_app.mysql, id)

    if not status:
        flash(message, "danger")
        return redirect(url_for("post.onaybekleyenler"))
    
    else:
        flash(message, "success")
        return redirect(url_for("post.blogindex"))

@post.before_request
def log_request_info():
    save_http_request()