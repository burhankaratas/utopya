from app.utils.logs import save_http_request
from app.utils.functions import login_required

from app.models.user_models import editprofile_model, ayarlar_get_model, ayarlar_post_model, changephoto_model, changepassword_model

from flask import Blueprint, session, request, render_template, flash, redirect, url_for, current_app

from werkzeug.utils import secure_filename
import uuid
import os

user = Blueprint('user', __name__)

@user.route("/edit", methods = ["GET", "POST"])
@login_required
def editprofile():
    if request.method == "GET":
        return render_template("editprofile.html")
    
    elif request.method == "POST":
        profileImage = request.files['profileImage']
        profileContent = request.form.get("profileContent")

        if profileImage.filename == '':
            flash("No selected file", "warning")
            return redirect(url_for("editprofile"))
        
        filename = secure_filename(profileImage.filename)
        random_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join("app/static/uploads", random_filename)
        profileImage.save(file_path)

        profile_image_url = f"/static/uploads/{random_filename}"

        status, message = editprofile_model(current_app.mysql, profile_image_url, profileContent)

        if not status:
            flash(message, "danger")
            return redirect(url_for("user.editprofile"))
        
        else:
            session["profileImage"] = profile_image_url

            flash(message, "success")
            return redirect(url_for("post.blogindex"))
        
@user.route("/ayarlar", methods = ["GET", "POST"])
@login_required
def ayarlar():
    if request.method == "GET":
        status, message = ayarlar_get_model(current_app.mysql)

        if not status:
            flash(message, "danger")
            return redirect(url_for("post.blogindex"))
        
        else:
            data = message

            return render_template("hesabim.html", data = data)
        
    elif request.method == "POST":
        userName = request.form.get("userName")
        name = request.form.get("name")
        surName = request.form.get("surName")
        email = request.form.get("email")
        profileContent = request.form.get("profileContent")

        status, message = ayarlar_post_model(current_app.mysql, userName, name, surName, email, profileContent)

        if not status:
            flash(message, "danger")
            return redirect(url_for("user.ayarlar"))
        
        else:
            flash(message, "success")
            return redirect(url_for("user.ayarlar"))
        
@user.route("/changephoto", methods = ["POST"])
@login_required
def changephoto():
    if request.method == "POST":
        profileImage = request.files['profileImage']

        if profileImage.filename == '':
            flash("Resim dosyası okunamadı. Tekrar yükleyin", "warning")
            return redirect(url_for("user.ayarlar"))
        
        filename = secure_filename(profileImage.filename)
        random_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join("app/static/uploads", random_filename)
        profileImage.save(file_path)

        profile_image_url = f"/static/uploads/{random_filename}"

        status, message = changephoto_model(current_app.mysql, profile_image_url)

        if not status:
            flash(message, "danger")
            return redirect(url_for("user.ayarlar"))
        
        else:
            flash(message, "success")
            return redirect(url_for("user.ayarlar"))
        
@user.route("/changepassword", methods = ["POST"])
@login_required
def changepassword():
    if request.method == "POST":
        latestpassword = request.form.get("lastpassword")

        newpassword = request.form.get("newpassword")
        newpasswordagain = request.form.get("newpasswordagain")

        if latestpassword == newpassword:
            flash("Şifreniz yeni şifreniz ile aynı olamaz", "danger")
            return redirect(url_for("user.ayarlar"))
        
        status, message = changepassword_model(current_app.mysql, latestpassword, newpassword, newpasswordagain)

        if not status:
            flash(message, "danger")
            return redirect(url_for("user.ayarlar"))
        
        else:
            flash(message, "success")
            return redirect(url_for("user.ayarlar"))

@user.before_request
def log_request_info():
    save_http_request()