from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from functools import wraps
from datetime import datetime
from config import KULLANICI_ADI, SIFRE  # config.py'den kullanıcı bilgileri

app = Flask(__name__)
app.secret_key = "gizli_anahtar"  # Bunu da mümkünse environment variable yapabilirsin

SESSION_TIMEOUT = 300  # 5 dakika (saniye cinsinden)

def db():
    conn = sqlite3.connect("apartman.db")
    conn.row_factory = sqlite3.Row
    return conn

# Oturum zaman aşımı kontrolü (5 dakika hareketsizlik)
@app.before_request
def oturum_zamani_kontrol():
    if "kullanici" in session:
        now = datetime.now().timestamp()
        son_istek = session.get("son_istek", now)

        if now - son_istek > SESSION_TIMEOUT:
            session.clear()
            return redirect(url_for("giris"))

        session["son_istek"] = now

# Giriş yapılmadıysa yönlendir
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "kullanici" not in session:
            return redirect(url_for("giris"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/giris", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        kullanici = request.form.get("kullanici")
        sifre = request.form.get("sifre")
        if kullanici == KULLANICI_ADI and sifre == SIFRE:
            session["kullanici"] = kullanici
            session["son_istek"] = datetime.now().timestamp()  # Oturum başlangıç zamanı
            return redirect(url_for("panel"))
        else:
            return render_template("giris.html", hata="Kullanıcı adı veya şifre hatalı")
    return render_template("giris.html")

@app.route("/cikis")
def cikis():
    session.clear()
    return redirect(url_for("giris"))

@app.route("/")
@login_required
def panel():
    return render_template("index.html", kullanici=session["kullanici"])

@app.route("/daireler", methods=["GET", "POST"])
@login_required
def daireler():
    conn = db()
    if request.method == "POST":
        no = request.form.get("daire_no")
        isim = request.form.get("isim")
        conn.execute("INSERT INTO daireler (daire_no, isim) VALUES (?, ?)", (no, isim))
        conn.commit()
    daireler = conn.execute("SELECT * FROM daireler").fetchall()
    return render_template("daireler.html", daireler=daireler)

@app.route("/daire_sil/<int:id>")
@login_required
def daire_sil(id):
    conn = db()
    conn.execute("DELETE FROM daireler WHERE id = ?", (id,))
    conn.commit()
    return redirect("/daireler")

@app.route("/aidatlar", methods=["GET", "POST"])
@login_required
def aidatlar():
    conn = db()
    if request.method == "POST":
        daire_id = request.form.get("daire_id")
        yeni_no = request.form.get("yeni_daire_no")
        yeni_isim = request.form.get("yeni_daire_isim")
        tutar = request.form.get("tutar")
        tarih = datetime.now().strftime("%Y-%m-%d")

        if yeni_no and yeni_isim:
            cur = conn.execute("INSERT INTO daireler (daire_no, isim) VALUES (?, ?)", (yeni_no, yeni_isim))
            conn.commit()
            daire_id = cur.lastrowid

        if not daire_id:
            return "Lütfen daire seçin ya da yeni girin", 400

        conn.execute("INSERT INTO aidatlar (daire_id, tutar, tarih, odendi) VALUES (?, ?, ?, 0)", (daire_id, tutar, tarih))
        conn.commit()

    daireler = conn.execute("SELECT * FROM daireler").fetchall()
    aidatlar = conn.execute("""
        SELECT a.id, d.daire_no, d.isim, a.tutar, a.tarih, a.odendi
        FROM aidatlar a JOIN daireler d ON a.daire_id = d.id
        ORDER BY a.tarih DESC
    """).fetchall()
    return render_template("aidatlar.html", aidatlar=aidatlar, daireler=daireler)

@app.route("/aidat_sil/<int:id>")
@login_required
def aidat_sil(id):
    conn = db()
    conn.execute("DELETE FROM aidatlar WHERE id = ?", (id,))
    conn.commit()
    return redirect("/aidatlar")

@app.route("/odendi/<int:id>")
@login_required
def odendi(id):
    conn = db()
    conn.execute("UPDATE aidatlar SET odendi = 1 WHERE id = ?", (id,))
    conn.commit()
    return redirect("/aidatlar")

@app.route("/giderler", methods=["GET", "POST"])
@login_required
def giderler():
    conn = db()
    if request.method == "POST":
        aciklama = request.form.get("aciklama")
        tutar = request.form.get("tutar")
        tarih = datetime.now().strftime("%Y-%m-%d")
        conn.execute("INSERT INTO giderler (aciklama, tutar, tarih) VALUES (?, ?, ?)", (aciklama, tutar, tarih))
        conn.commit()
    giderler = conn.execute("SELECT * FROM giderler").fetchall()
    return render_template("giderler.html", giderler=giderler)

@app.route("/gider_sil/<int:id>")
@login_required
def gider_sil(id):
    conn = db()
    conn.execute("DELETE FROM giderler WHERE id = ?", (id,))
    conn.commit()
    return redirect("/giderler")

@app.route("/rapor")
@login_required
def rapor():
    conn = db()
    borclar = conn.execute("""
        SELECT d.daire_no, d.isim, a.tutar, a.tarih
        FROM aidatlar a JOIN daireler d ON a.daire_id = d.id
        WHERE a.odendi = 0
    """).fetchall()
    giderler = conn.execute("SELECT * FROM giderler").fetchall()
    return render_template("rapor.html", borclar=borclar, giderler=giderler)


if __name__ == "__main__":
    app.run(debug=False)
