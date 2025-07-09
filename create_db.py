import sqlite3

def create_db():
    conn = sqlite3.connect('apartman.db')
    c = conn.cursor()

    # Daireler tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS daireler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daire_no TEXT NOT NULL,
            isim TEXT NOT NULL
        )
    ''')

    # Aidatlar tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS aidatlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            daire_id INTEGER NOT NULL,
            tutar REAL NOT NULL,
            tarih TEXT NOT NULL,
            odendi INTEGER DEFAULT 0,
            FOREIGN KEY (daire_id) REFERENCES daireler(id)
        )
    ''')

    # Giderler tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS giderler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aciklama TEXT NOT NULL,
            tutar REAL NOT NULL,
            tarih TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar oluşturuldu.")

if __name__ == '__main__':
    create_db()
