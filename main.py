from flask import render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import uuid

import base64
import os

from config import create_app, init_mysql
from views.functions import login_required, date, generate_url, admin_required

SITE_URL = "http://localhost"

app = create_app()
mysql = init_mysql(app)

@app.route("/")
def index():
    if "logged_in" in session:
        if session["IsVerified"] == 1:
            return redirect(url_for("yazilar"))
    
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM articles WHERE IsPublish = 1 ORDER BY id DESC"
    result = cursor.execute(query)

    if result > 0:
        datas = cursor.fetchall()
        cursor.close()

        return render_template("index.html", datas = datas)
    
    else:
        cursor.close()
        datas = None
        return render_template("index.html", datas = datas)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        userName = request.form.get("username")
        password = request.form.get("password")

        cursor = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE userName = %s"
        result = cursor.execute(query, (userName,))

        if result > 0:
            data = cursor.fetchone()

            IsAdmin = data['IsAdmin']

            if sha256_crypt.verify(password, data['password']):
                if IsAdmin == 0:
                    cursor.close()

                    
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
                        cursor.close()
                        return redirect(url_for("index"))

                else:
                    cursor.close()
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
                        cursor.close()
                        return redirect(url_for("index"))
                
            else:
                cursor.close()
                flash("Hatalı Şifre.", "danger")
                return redirect(url_for("login"))

        else:
            cursor.close()
            flash("Kullanıcı bulunamadı", "danger")
            return redirect(url_for("login"))

    else:
        return "Error"

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/edit", methods=["GET", "POST"])
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)
        profileImage.save(file_path)

        profile_image_url = f"/{file_path}"

        cursor = mysql.connection.cursor()

        query = "UPDATE users SET profileImage = %s, profileContent = %s, IsVerified = 1 WHERE id = %s"
        cursor.execute(query, (profile_image_url, profileContent, session['id']))

        if cursor.rowcount > 0:
            mysql.connection.commit()
            cursor.close()

            session["IsVerified"] = 1

            flash("Tebrikler Profiliniz Hazır!", "success")
            return redirect(url_for("index"))
        
        else:
            cursor.close()

            flash("Beklenmedik bir hata. Lütfen tekrar deneyiniz.", "warning")
            return redirect(url_for("editprofile"))

@app.route("/yazilarim")
@login_required
def yazilar():
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM articles WHERE writer = %s"
    result = cursor.execute(query, (session['userName'],))

    if result > 0:
        datas = cursor.fetchall()

        return render_template("yazilarim.html", datas = datas)
    
    else:
        datas = ""
        return render_template("yazilarim.html", datas = datas)

@app.route("/yazi-yaz", methods=["GET", "POST"])
@login_required
def yaziekle():
    if request.method == "GET":
        return render_template("yaziyaz.html")
    
    elif request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        hastag = request.form.get("hastag")

        blogContent = request.form.get("blogContent")
        articleLogo = request.files['articleLogo']
        
        if articleLogo.filename == "":
            flash('Makale logosu alınamadı. Lütfen tekrar giriniz.', "danger")
            return redirect(url_for("yaziekle"))

        articleLogor = base64.b64encode(articleLogo.read()).decode('utf-8')
        writer = session['userName']
        createdDate = date()
        url = generate_url(title)

        cursor = mysql.connection.cursor()

        query = "INSERT INTO articles (title, content, blogContent, articleLogo, writer, createdDate, url, hastag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (title, content, blogContent, articleLogor, writer, createdDate, url, hastag))

        if cursor.rowcount > 0:
            mysql.connection.commit()
            cursor.close()
            flash("Yazınız Yetkili Ekibe İletildi! Yetkililer tarafından onaylandığında yazınız herkese açık olacaktır!", "success")
            return redirect(url_for("yazilar"))
        
        else:
            cursor.close()
            flash("Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz. Sorun tekrar ederse bize bildirin", "danger")
            return redirect(url_for("yaziekle"))
        
@app.route("/@<userName>")
def profile(userName):
    try:
        cursor = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE userName = %s"
        result = cursor.execute(query, (userName,))

        if result > 0:
            data = cursor.fetchone()

            query2 = "SELECT * FROM articles WHERE writer = %s AND IsPublish = 1 ORDER BY id DESC"
            result2 = cursor.execute(query2, (userName,))

            if result2 > 0:
                gonderidatas = cursor.fetchall()

            else:
                gonderidatas = ""


            return render_template("profile.html", data = data, userName = userName, gonderidatas = gonderidatas)

        else:
            cursor.close()

            flash("Böyle bir hesap bulamadık! Lütfen doğru isim olduğundan emin olun", "warning")
            return redirect(url_for("index"))

    except:
        return "Beklenmedik bir hata var! Lütfen tekrar deneyiniz. Devam ederse bize bildirin."

@app.route("/p/<url>")
def yazi(url):
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM articles WHERE url = %s"
    result = cursor.execute(query, (url,)) 

    if result > 0:
        data = cursor.fetchone()

        if data['IsPublish'] == 1:
            query2 = "SELECT * FROM users WHERE userName = %s"
            result2 = cursor.execute(query2, (data['writer'],))

            if result2 > 0:
                user = cursor.fetchone()
                profileImage = user['profileImage']

                return render_template("yazi.html", data = data, profileImage = profileImage, user = user)

            else:
                return render_template("yazi.html", data = data)
        
        else:
            flash("Böyle bir makale bulunamadı. Lütfen tekrar deneyin", "warning")
            return redirect(url_for("index"))        

    else:
        flash("Böyle bir makale bulunamadı. Lütfen tekrar deneyin", "warning")
        return redirect(url_for("index"))   
    
@app.route("/gonderi-guncelle/<id>", methods = ['GET', "POST"])
def gonderiguncelle(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE id = %s"
        result = cursor.execute(query, (id,))

        if result > 0:
            data = cursor.fetchone()
            cursor.close()

            return render_template("gonderiguncelle.html", data = data)

        else:
            cursor.close()

            flash("Böyle bir gönderi yok. Lütfen tekrar dene.", "danger")
            return redirect(url_for("yazilar"))
    
    elif request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        blogContent = request.form.get('blogContent')
        hastag = request.form.get('hastag')

        cursor = mysql.connection.cursor()

        query = "UPDATE articles SET title = %s, content = %s, blogContent = %s, hastag = %s, IsPublish = 0 WHERE id = %s"
        cursor.execute(query, (title, content, blogContent, hastag, id))

        if cursor.rowcount > 0:
            mysql.connection.commit()
            cursor.close()

            flash("Yazınız Güncellendi. Tekrar herkese açık olmadan önce lütfen yetkililerden tekrar yayıma alınmasını isteyin", "success")
            return redirect(url_for("yazilar"))

        else:
            cursor.close()

            flash("Güncelleme başarısız. Tekrar deneyin devam ederse yetkililere iletin", "warning")
            return redirect(url_for("yazilar"))

    else:
        return "Yokk"

@app.route("/delete/<id>")
def yazisil(id):
    cursor = mysql.connection.cursor()

    query = "DELETE FROM articles WHERE id = %s"
    cursor.execute(query, (id))

    if cursor.rowcount > 0:
        mysql.connection.commit()
        cursor.close()

        flash("Gönderi silindi", "success")
        return redirect(url_for("yazilar"))

    else:
        cursor.close()

        flash("Gönderi silinemedi", "danger")
        return redirect(url_for("yazilar"))

@app.route("/yazarlar")
def yazarlar():
    cursor = mysql.connection.cursor()

    query = "SELECT * FROM users"
    result = cursor.execute(query)
    
    if result > 0:
        datas = cursor.fetchall()

        return render_template("yazarlar.html", datas = datas)
    
    else:
        datas = None

        return render_template("yazarlar.html", datas = datas)


@app.route("/hakkimizda")
def hakkimizda():
    return render_template("hakkimizda.html")

@app.route("/iletisim")
def iletisim():
    return render_template("iletisim.html")

@app.route("/onay-bekleyenler")
@admin_required
def onaybekleyenler():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE IsPublish = 0"
    result = cursor.execute(query)

    if result > 0:
        datas = cursor.fetchall()
        cursor.close()

        return render_template("onaybekleyenler.html", datas = datas)

    else:
        cursor.close()

        flash("Şuanda onay bekleyen yazı bulunmamaktadır", "danger")
        
        return redirect(url_for("yazilar"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50))
    app.run(host="0.0.0.0", port=port, debug=True)