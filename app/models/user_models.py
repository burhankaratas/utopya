from app.utils.logs import save_error
from passlib.hash import sha256_crypt

from flask import session

def editprofile_model(mysql, profile_image_url, profileContent):
    try:
        cur = mysql.connection.cursor()

        query = "UPDATE users SET profileImage = %s,    profileContent = %s, IsVerified = 1 WHERE id = %s"
        cur.execute(query, (profile_image_url, profileContent,  session["id"]))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            session["IsVerified"] = 1

            return True, "Tebrikler Profiliniz Hazır!"

        else:
            cur.close()

            return False, "Beklenmedik bir hata. Lütfen tekrar deneyiniz."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def ayarlar_get_model(mysql):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE id = %s"
        result = cur.execute(query, (session['id'],))

        if result > 0:
            data = cur.fetchone()
            cur.close()

            return True, data

        else:
            cur.close()
            return False, "Beklenmedik bir hata oluştu"
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def ayarlar_post_model(mysql, userName, name, surName, email, profileContent):
    try:
        cur = mysql.connection.cursor()
        
        fristquery = "SELECT * FROM users WHERE id = %s"
        result = cur.execute(fristquery, (session['id'],))

        data = cur.fetchone()

        if userName == data['userName'] and name == data['name'] and surName == data['surName'] and email == data['email'] and profileContent == data['profileContent']:
            return False, "Değişiklik yapılmadı. Herhangi bir güncelleme işlemi gerçekleştirilmedi"
        
        query = "UPDATE users SET userName = %s, name = %s, surName = %s, email = %s, profileContent = %s WHERE id = %s"

        cur.execute(query, (userName, name, surName, email, profileContent, session['id']))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()
            
            return True, "Hesap bilgileriniz başarıyla güncellendi."
        
        else:
            cur.close()

            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz"

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere bildirildi."
    

def changephoto_model(mysql, profile_image_url):
    try:
        cur = mysql.connection.cursor()

        query = "UPDATE users SET profileImage = %s WHERE id = %s"
        cur.execute(query, (profile_image_url, (session['id'],)))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            session['profileImage'] = profile_image_url

            return True, "Profil fotoğrafınız başarıyla güncellendi!"
        
        else:
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz"


    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere bildirildi."

def changepassword_model(mysql, latestpassword, newpassword, newpasswordagain):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT password FROM users WHERE id = %s"
        result = cur.execute(query, (session["id"],))

        if result > 0:
            data = cur.fetchone()

            if sha256_crypt.verify(latestpassword, data["password"]):
                if newpassword != newpasswordagain:
                    return False, "Şifreler birbiri ile uyuşmuyor. Lütfen tekrar deneyiniz"
                
                hashedpassword = sha256_crypt.encrypt(newpassword)

                query2 = "UPDATE users SET password = %s WHERE id = %s"
                cur.execute(query2, (hashedpassword, session["id"],))

                if cur.rowcount > 0:
                    mysql.connection.commit()
                    cur.close()

                    return True, "Şifreniz başarıyla güncellendi"

                else:
                    cur.close()

                    return False, "Beklenmedik bir hata. Lütfen tekrar deneyiniz"

            else:
                cur.close()

                return False, "Eski şifre hatalı"
        
        else:
            cur.close()
            
            return False, "Beklenmedik bir hata ile karşılaşıldı"

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere bildirildi."