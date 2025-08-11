# Python Kütüphane Yönetim Sistemi

Bu proje, SQLite veritabanı kullanan basit ve etkili bir kütüphane yönetim sistemidir. Kitap ekleme, silme, güncelleme, sorgulama, ödünç verme ve iade alma işlemleri yapılabilmekte; yapılan işlemler loglanmaktadır.

---

## Özellikler

- **Kitap Ekleme:** Yeni kitap bilgilerini veritabanına ekler.
- **Kitap Silme:** Var olan kitapları veritabanından kaldırır.
- **Kitap Güncelleme:** Kitap bilgilerini güncelleyebilir.
- **Kitap Sorgulama:** Kitapları belirli kriterlere göre arayabilir.
- **Kitap Listesi:** Kütüphanedeki tüm kitapları listeler.
- **Ödünç Verme / İade Alma:** Kitap ödünç verme ve iade işlemlerini takip eder.
- **Loglama:** Tüm işlemler `log.db` veritabanına kaydedilir.
- **Geliştirici Modu:** Özel bir kod (`5348`) ile gelişmiş yönetim moduna geçiş yapılabilir.

---

## Kurulum

1. Python 3.x sürümü yüklü olmalıdır.
2. Proje dosyalarını indirin veya klonlayın.
3. Gerekli Python standart kütüphaneleri (`sqlite3`, `time`, `os`, `platform`) kurulu olmalıdır (Python ile birlikte gelir).

---

## Kullanım

Terminal veya komut satırında proje klasörüne gidip:

```bash python main.py ```

Program çalışmaya başlayacaktır.

---

## Menü İşlemleri

- Kitap Ekle  
- Kitap Sil  
- Kitapları Listele  
- Kitap Arama  
- Kitap Ödünç Verme  
- Kitap İade Alma  
- Çıkış  

---

## Geliştirici Modu

Ana menüde, işlemler yerine **5348** kodu girildiğinde, geliştirici moduna geçilir. Bu modda;  

- Veritabanı bağlantısı açılabilir veya kapatılabilir.  
- İşlem logları görüntülenebilir.  

---

## Veritabanları

- `veritabani.db` : Kitap verileri tutulur.  
- `log.db` : Yapılan işlemlerin kaydı tutulur.  

---

## Proje Dosyaları

- `backend.py` : Kütüphane ve kitap işlemlerini gerçekleştiren sınıflar.  
- `main.py` : Kullanıcı arayüzü ve komut satırı işlemleri.  

---

## İletişim

Her türlü soru ve öneri için bana ulaşabilirsiniz.  

---

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
