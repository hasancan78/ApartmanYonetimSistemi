🏢 Apartman Yönetim Sistemi
Bu proje, apartman yöneticilerinin aidat, gider, daire ve rapor işlemlerini kolayca takip edebilmesi için geliştirilmiş basit bir web tabanlı yönetim sistemidir. Flask framework'ü kullanılarak PythonAnywhere üzerinde yayınlanmıştır.

🚀 Özellikler
🧾 Aidat takibi ve listeleme

📊 Giderlerin kaydı ve görüntülenmesi

🏠 Daire bilgilerini yönetme

🔐 Giriş ekranı ile yetkilendirme

📄 Rapor sayfası

🌐 PythonAnywhere üzerinde çevrimiçi kullanım

🔧 Kullanılan Teknolojiler
Python 3.x

Flask

SQLite

HTML & Jinja2

Bootstrap (şablonlarda)

PythonAnywhere (yayın ortamı)

🗂️ Dosya Yapısı
pgsql
Kopyala
Düzenle
apartman-yonetim-sistemi/
├── app.py
├── create_db.py
├── apartman.db  (veritabanı, sürüm kontrolüne dahil edilmemiştir)
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── index.html
│   ├── aidatlar.html
│   ├── giderler.html
│   ├── daireler.html
│   └── rapor.html
└── README.md
📁 Veritabanı Oluşturma ve Çalıştırma
Projede kullanılan SQLite veritabanı dosyası (apartman.db) sürüm kontrolüne dahil edilmemiştir. Bu nedenle, projeyi çalıştırmadan önce veritabanının oluşturulması gerekmektedir.

Veritabanını oluşturmak için projenin ana dizininde create_db.py adlı bir Python dosyası bulunmaktadır. Bu dosya çalıştırıldığında, ihtiyaç duyulan tablolar otomatik olarak oluşturulur.

Veritabanı oluşturma adımları:

Terminal veya komut satırında projenin ana dizinine gidin.

Aşağıdaki komutu çalıştırın:

bash
Kopyala
Düzenle
python create_db.py
Veritabanı ve tablolar oluşturulduktan sonra uygulamayı başlatabilirsiniz:

bash
Kopyala
Düzenle
python app.py
Bu yöntemle veritabanını kolayca oluşturabilir ve uygulamayı sorunsuz çalıştırabilirsiniz.

🌍 Canlı Demo
Aşağıdaki bağlantı üzerinden canlı olarak erişebilirsiniz:

👉 https://hasanck.pythonanywhere.com

ℹ️ Proje Hakkında
Bu proje, kişisel öğrenme ve geliştirme amaçlı hazırlanmıştır. Apartman yönetimi ile ilgili temel işlevleri kolay ve kullanışlı bir arayüzle sunmayı hedeflemekteyim. Projeyi geliştirirken Flask framework'ünü öğrenme, web tabanlı CRUD işlemleri yapma ve basit kullanıcı doğrulama sistemleri geliştirme konularında kendimi geliştirdim.
