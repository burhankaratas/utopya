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
            return redirect(url_for("blogindex"))
    
    cursor = mysql.connection.cursor()

    query = "SELECT title, content, writer, url, createdDate, hastag FROM articles WHERE IsPublish = 1 ORDER BY id DESC"
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

    query = "SELECT * FROM articles WHERE writer = %s AND IsDraft = 0"
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
        
    
        writer = session['userName']
        createdDate = date()
        url = generate_url(title)

        cursor = mysql.connection.cursor()

        query = "INSERT INTO articles (title, content, blogContent, writer, createdDate, url, hastag, IsDraft) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)"
        cursor.execute(query, (title, content, blogContent, writer, createdDate, url, hastag))

        if cursor.rowcount > 0:
            mysql.connection.commit()
            cursor.close()
            flash("Yazınız taslak olarak kaydedildi. Taslaklardan yazınızı yayım için gönderebilir veya ön izlemesini görebilirsiniz", "success")
            return redirect(url_for("taslaklar"))
        
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
@login_required
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
@login_required
def yazisil(id):
    cursor = mysql.connection.cursor()

    query = "DELETE FROM articles WHERE id = %s"
    cursor.execute(query, (id,))

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

@app.route("/onay-bekleyenler")
@admin_required
def onaybekleyenler():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE IsPublish = 0 AND IsDraft = 0"
    result = cursor.execute(query)

    if result > 0:
        datas = cursor.fetchall()
        cursor.close()

        return render_template("onaybekleyenler.html", datas = datas)

    else:
        cursor.close()

        flash("Şuanda onay bekleyen yazı bulunmamaktadır", "danger")
        
        return redirect(url_for("yazilar"))
    

@app.route("/publish/<id>")
@admin_required
def publishwait(id):
    cursor = mysql.connection.cursor()

    query = "UPDATE articles SET IsPublish = 1 WHERE id = %s"
    cursor.execute(query, (id,))

    if cursor.rowcount > 0:
        mysql.connection.commit()
        cursor.close()

        flash("Yazı şuan herkese açık olarak yayımlandı!", "success")
        return redirect(url_for("index"))

    else:
        cursor.close()

        flash("Gönderi zaten yayımda veya bir hata oluştu. Devam ederse site yetkililerine bildiriniz", "danger")
        return redirect(url_for("index"))
    
@app.route("/ayarlar", methods = ["GET", "POST"])
@login_required
def ayarlar():
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE id = %s"
        result = cursor.execute(query, (session['id'],))

        if result > 0:
            data = cursor.fetchone()

            cursor.close()

            return render_template("hesabim.html", data = data)

        else:
            cursor.close()
            flash("Beklenmedik bir hata oluştu.", "danger")
            return redirect(url_for("blogindex"))
        
    elif request.method == "POST":
        userName = request.form.get("userName")
        name = request.form.get("name")
        surName = request.form.get("surName")
        email = request.form.get("email")
        profileContent = request.form.get("profileContent")

        cur = mysql.connection.cursor()

        fristquery = "SELECT * FROM users WHERE id = %s"
        result = cur.execute(fristquery, (session["id"],))

        data = cur.fetchone()

        if userName == data['userName'] and name == data['name'] and surName == data        ['surName'] and email == data['email'] and profileContent == data['profileContent']:
            flash("Değişiklik yapılmadı. Herhangi bir güncelleme işlemi gerçekleştirilmedi.", "info")
            return redirect(url_for("blogindex"))

        query = "UPDATE users SET userName = %s, name = %s, surName = %s, email = %s, profileContent = %s WHERE id = %s"

        cur.execute(query, (userName, name, surName, email, profileContent, session["id"]))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            flash("Hesap bilgileriniz başarıyla güncellendi!", "success")
            return redirect(url_for("blogindex"))
        
        else:
            cur.close()

            flash("Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyin.", "danger")


@app.route("/index")
@login_required
def blogindex():
    return render_template("blogindex.html")


@app.route("/changephoto", methods = ["POST"])
@login_required
def changephoto():
    if request.method == "POST":
        profileImage = request.files['profileImage']

        if profileImage.filename == '':
            flash("Resim dosyası okunamadı. Tekrar yükleyin", "warning")
            return redirect(url_for("ayarlar"))
        
        filename = secure_filename(profileImage.filename)
        random_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_filename)
        profileImage.save(file_path)

        profile_image_url = f"/{file_path}"

        cur = mysql.connection.cursor()

        query = "UPDATE users SET profileImage = %s WHERE id = %s"
        cur.execute(query, (profile_image_url, (session["id"],)))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            session["profileImage"] = profile_image_url

            flash("Profil fotoğrafınız başarıyla güncellendi!", "success")
            return redirect(url_for("ayarlar"))
        
        else:
            flash("Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz", "danger")
            return redirect(url_for("ayarlar"))

@app.route("/changepassword", methods = ["POST"])
@login_required
def changepassword():
    if request.method == "POST":
        latestpassword = request.form.get("lastpassword")

        newpassword = request.form.get("newpassword")
        newpasswordagain = request.form.get("newpasswordagain")

        if latestpassword == newpassword:
            flash("Şifreniz yeni şifreniz ile aynı olamaz", "danger")
            return redirect(url_for("ayarlar"))

        cur = mysql.connection.cursor()

        query = "SELECT password FROM users WHERE id = %s"
        result = cur.execute(query, (session["id"],))

        if result > 0:
            data = cur.fetchone()

            if sha256_crypt.verify(latestpassword, data["password"]):
                if newpassword != newpasswordagain:
                    flash("Şifreler birbiri ile uyuşmuyor. Lütfen tekrar deneyiniz", "danger")
                    return redirect(url_for("ayarlar"))
                
                hashedpassword = sha256_crypt.encrypt(newpassword)

                query2 = "UPDATE users SET password = %s WHERE id = %s"
                cur.execute(query2, (hashedpassword, session["id"],))

                if cur.rowcount > 0:
                    mysql.connection.commit()
                    cur.close()

                    flash("Şifreniz başarıyla güncellendi", "success")
                    return redirect(url_for("ayarlar"))

                else:
                    cur.close()

                    flash("Beklenmedik bir hata. Lütfen tekrar deneyiniz", "danger")
                    return redirect(url_for("ayarlar")) 

            else:
                cur.close()

                flash("Eski şifre hatalı", "danger")
                return redirect(url_for("ayarlar"))
        
        else:
            cur.close()

            flash("Beklenmedik bir hata ile karşılaşıldı", "danger")
            return redirect(url_for("ayarlar"))
        
@app.route("/taslaklar")
@login_required
def taslaklar():
    cur = mysql.connection.cursor()

    query = "SELECT id, title, content, writer, watch, url, createdDate, hastag FROM articles WHERE writer = %s AND IsDraft = 1"

    result = cur.execute(query, (session["userName"],))

    if result > 0:
        datas = cur.fetchall()
        cur.close()

        return render_template("taslaklar.html", datas = datas)
        

    else:
        cur.close()

        flash("Herhangi bir taslak bulunmamakta", "warning")
        return redirect(url_for("blogindex"))
    

@app.route("/taslak/<id>")
@login_required
def taslak(id):
    cur = mysql.connection.cursor()

    query = "SELECT * FROM articles WHERE id = %s"
    result = cur.execute(query, (id,))

    if result > 0:
        data = cur.fetchone()
        cur.close()

        return render_template("yazi.html", data = data)

    else:
        cur.close()

        flash("Taslak bulunamadı", "warning")
        return redirect(url_for("taslaklar"))
    

@app.route("/pub/<id>")
def pubrequest(id):
    cur = mysql.connection.cursor()
    
    query = "UPDATE articles SET IsDraft = 0 WHERE id = %s"
    cur.execute(query, (id,))

    if cur.rowcount > 0:
        mysql.connection.commit()
        cur.close()

        flash("Yayım için yöneticilere gönderildi", "success")
        return redirect(url_for("blogindex"))
    
    else:
        cur.close()

        flash("Beklenmedik bir hata. Lütfen tekrar deneyin", "danger")
        return redirect(url_for("blogindex"))
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50))
    app.run(host="0.0.0.0", port=port, debug=True)