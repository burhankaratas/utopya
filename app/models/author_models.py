from passlib.hash import sha256_crypt
from app.utils.logs import save_error

def login_model(mysql, userName, password):
    try:
        cur = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE userName = %s"
        result = cur.execute(query, (userName,))

        if result > 0:
            data = cur.fetchone()

            if sha256_crypt.verify(password, data['password']):
                return True, data

            else:
                return False, "Hatalı Şifre"
        else:
            return False, "Kullanıcı Bulunamadı"
        
    
    except Exception as e:
        save_error(str(e))
        return False, "Beklenmedik bir hata ile karşılaşıldı. Hata yetkililere iletildi."