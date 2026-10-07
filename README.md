# Ütopya

> Çok yazarlı, onay akışlı bir dijital yazı ve blog platformu.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![Lisans](https://img.shields.io/badge/license-MIT-green)

Ütopya; yazarların yazı yazıp taslak olarak saklayabildiği, yayına gönderebildiği
ve editör onayından sonra yayınlandığı bir platformdur. Kullanıcı profilleri,
yazar sayfaları ve mesajlaşma ile birlikte uçtan uca bir yayın deneyimi sunar.

## Özellikler

- **Kayıt / giriş sistemi** — oturum yönetimi ve şifre değiştirme.
- **Yazı yazma & taslak** — yazı oluşturma, taslak olarak saklama, güncelleme, silme.
- **Yayın onay akışı** — yazar yayın talebi gönderir, editör onaylar; onay bekleyen
  içerikler ayrı ekranda listelenir.
- **Yazar sayfaları** — yazarlar listesi ve bireysel yazar profilleri.
- **Kullanıcı profili** — profil düzenleme, fotoğraf ve şifre güncelleme.
- **Mesajlaşma / bildirim** — kullanıcılar arası mesaj ekranı.

## Teknoloji Yığını

| Katman | Kullanılan |
|---|---|
| Backend | Python 3.12, Flask 3 (Blueprint mimarisi) |
| Veritabanı | MySQL, `flask-mysqldb` (ham SQL + `DictCursor`) |
| Şablonlar | Jinja2, Bootstrap |
| Ön yüz | HTML, CSS, JavaScript (Owl Carousel) |
| Ortam | python-dotenv |

## Dizin Yapısı

```
utopya/
├── run.py                     # Giriş noktası
├── config.py                  # Yapılandırma + MySQL başlatma
├── requirements.txt
├── app/
│   ├── __init__.py            # Uygulama fabrikası, blueprint kaydı
│   ├── controllers/           # user / author / post / main route'ları
│   ├── models/                # Veritabanı işlemleri
│   ├── templates/             # Jinja2 şablonları
│   └── static/                # CSS, JS, görseller
└── .env.example
```

## Kurulum

Gereksinimler: **Python 3.10+** ve **MySQL 5.7+/8+**.

```bash
# 1) Sanal ortam
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2) Bağımlılıklar
pip install -r requirements.txt

# 3) Veritabanı
mysql -u root -p -e "CREATE DATABASE utopya CHARACTER SET utf8mb4;"

# 4) Ortam değişkenleri
cp .env.example .env          # değerleri kendinize göre düzenleyin

# 5) Çalıştır
python run.py
```

Uygulama varsayılan olarak `http://localhost:5000` üzerinde açılır.

## Ortam Değişkenleri

`.env` dosyasında tanımlanır: `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`,
`MYSQL_DB`, `SECRET_KEY`.

## Lisans

MIT — bkz. [LICENSE](LICENSE).