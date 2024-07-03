from app.utils.logs import save_error
from flask import session

def yazilar_model(mysql):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE writer = %s AND   IsDraft = 0"
        result = cur.execute(query, (session['userName'],))

        if result > 0:
            datas = cur.fetchall()

            return True, datas

        else:
            datas = ""

            return True, datas
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."

def yaziekle_model(mysql, title, content, blogContent, writer, createdDate, url, hastag):
    try:
        cur = mysql.connection.cursor()

        query = "INSERT INTO articles (title, content, blogContent, writer, createdDate, url, hastag, IsDraft) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)"
        cur.execute(query, (title, content, blogContent, writer, createdDate, url, hastag))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            return True, "Yazınız taslak olarak kaydedildi. Taslaklardan yazınızı yayım için gönderebilir veya ön izlemesini görebilirsiniz"

        else:
            cur.close()
            return False, "Beklenmedik bir hata ile karşılaşıldı. Lütfen tekrar deneyiniz. Sorun tekrar ederse bize bildirin"

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."

def taslaklar_model(mysql):
    try:
        cur = mysql.connection.cursor()
    
        query = "SELECT id, title, content, writer, watch, url, createdDate, hastag FROM articles WHERE writer = %s AND IsDraft = 1"
    
        result = cur.execute(query, (session['userName'],))
    
        if result > 0:
            datas = cur.fetchall()
            cur.close()
    
            return True, datas
    
        else:
            cur.close()
            return False, "Herhangi bir taslak bulunmamaktadır."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def gonderi_guncelle_get_model(mysql, id):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE id = %s"
        result = cur.execute(query, (id,))

        if result > 0:
            data = cur.fetchone()
            cur.close()

            return True, data

        else:
            cur.close()
            return False, "Böyle bir gönderi yok. Lütfen tekrar deneyiniz."

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def gonderi_guncelle_post_model(mysql, title, content, blogContent, hastag, id):
    try:
        cur = mysql.connection.cursor()

        query = "UPDATE articles SET title = %s, content = %s, blogContent = %s, hastag = %s, IsPublish = 0 WHERE id = %s"
        cur.execute(query, (title, content, blogContent, hastag, id))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            return True, "Yazınız Güncellendi. Tekrar herkese açık olmadan önce lütfen yetkililerden tekrar yayıma alınmasını isteyin"

        else:
            cur.close()
            return False, "Güncelleme başarısız. Tekrar deneyin devam ederse yetkililere iletin"

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def yazisil_model(mysql, id):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT writer FROM articles WHERE id = %s"
        result = cur.execute(query, (id,))

        if result > 0:
            data = cur.fetchone()

            writer = data['writer']

            if writer != session['userName']:
                cur.close()

                return False, "Başkasına ait bir gönderiyi  silemezsiniz!"

            query2 = "DELETE FROM articles WHERE id = %s"
            cur.execute(query2, (id,))

            if cur.rowcount > 0:
                mysql.connection.commit()
                cur.close()

                return True, "Gönderi silindi"

            else:
                cur.close()

                return False, "Gönderi silinemedi"

        else:
            return False, "Beklenmedik bir hata oluştu. Lütfen tekrar deneyiniz."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def taslak_model(mysql, id):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE id = %s"
        result = cur.execute(query, (id,))

        if result > 0:
            data = cur.fetchone()
            cur.close()

            return True, data

        else:
            cur.close()

            return False, "Taslak bulunamadı"
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def pubrequest_model(mysql, id):
    try:
        cur = mysql.connection.cursor()

        query = "UPDATE articles SET IsDraft = 0 WHERE id = %s"
        cur.execute(query, (id,))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            return True, "Yayım için yöneticilere gönderildi"

        else:
            cur.close()

            return False, "Beklenmedik bir hata. Lütfen tekrar deneyin."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def onaybekleyenler_model(mysql):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE IsPublish = 0 AND     IsDraft = 0"
        result = cur.execute(query)

        if result > 0:
            datas = cur.fetchall()
            cur.close()

            return True, datas

        else:
            cur.close()

            return False, "Şuanda onay bekleyen yazı bulunmamaktadır."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    

def publishwait_model(mysql, id):
    try:
        cur = mysql.connection.cursor()

        query = "UPDATE articles SET IsPublish = 1 WHERE id = %s"
        cur.execute(query, (id,))

        if cur.rowcount > 0:
            mysql.connection.commit()
            cur.close()

            return True, "Yazı şuan herkese açık olarak     yayımlandı!"

        else:
            cur.close()

            return False, "Gönderi zaten yayımda veya bir hata oluştu. Devam ederse site yetkililerine bildiriniz."
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
