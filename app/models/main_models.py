from app.utils.logs import save_error

def index_model(mysql):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT title, content, writer, url, createdDate, hastag FROM articles WHERE IsPublish = 1 ORDER BY id DESC"
        result = cur.execute(query)

        if result > 0:
            datas = cur.fetchall()
            cur.close()

            return True, datas

        else:
            cur.close()
            datas = None

            return True, datas
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def yazarlar_model(mysql):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM users"
        result = cur.execute(query)

        if result > 0:
            datas = cur.fetchall()
            cur.close()

            return True, datas

        else:
            datas = None

            return True, datas
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."
    
def yazi_model(mysql, url):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM articles WHERE url = %s"
        cur.execute(query, (url,))
        data = cur.fetchone()

        if data and data['IsPublish'] == 1:
            query2 = "SELECT * FROM users WHERE userName = %s"
            cur.execute(query2, (data['writer'],))
            user = cur.fetchone()

            if user:
                profileImage = user['profileImage']
            else:
                profileImage = None

            return True, data, profileImage, user

        else:
            return False, "Böyle bir makale bulunamadı.", None, None

    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi.", None, None
    
def profile_model(mysql, userName):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE userName = %s"
        result = cur.execute(query, (userName,))

        if result > 0:
            data = cur.fetchone()

            query2 = "SELECT title, content, writer, url,   createdDate, hastag FROM articles WHERE writer = %s   AND IsPublish = 1 ORDER BY id DESC"
            result2 = cur.execute(query2, (userName,))

            if result2 > 0:
                gonderidatas = cur.fetchall()
                cur.close()

            else:
                gonderidatas = ""

            return True, data, gonderidatas

        else:
            cur.close()

            return False, "Böyle bir hesap bulamadık! Lütfen doğru isim olduğundan emin olun", None
        
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi.", None