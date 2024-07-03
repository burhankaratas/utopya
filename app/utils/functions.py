from flask import session, flash, redirect, url_for
from datetime import datetime
from functools import wraps

import re

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntüleme izniniz yok", "danger")
            return redirect(url_for("index"))
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            if session['IsAdmin'] == 1:
                return f(*args, **kwargs)
            
            else:
                flash("Bu sayfayı görüntüleme izniniz yok", "danger")
                return redirect(url_for("index"))
        else:
            flash("Bu sayfayı görüntüleme izniniz yok", "danger")
            return redirect(url_for("index"))
    return decorated_function


def date():
    now = datetime.now()
    
    turkish_months = [
        "Ocak", "Şubat", "Mart", "Nisan",
        "Mayıs", "Haziran", "Temmuz", "Ağustos",
        "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    
    turkish_date = f"{now.day} {turkish_months[now.month - 1]} {now.year}"
    
    return turkish_date

def generate_url(title):
    title = title.lower()

    title = re.sub(r'[^a-z0-9]+', '-', title)

    title = title.strip('-')
    return title