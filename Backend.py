import sqlite3
import time

class kitap():
    def __init__(self,ad,yazar,yili,dagitim,baski,tarih,buradami=1,kimde=None):
        self.ad = ad
        self.yazar = yazar
        self.yili = yili
        self.dagitim = dagitim
        self.baski = baski
        self.tarih = tarih if tarih else time.strftime("%Y-%m-%d %H:%M:%S")  # Tarih bilgisi yoksa mevcut tarih kullanılır
        self.burdami = buradami
        self.kimde = kimde

    def __str__(self):
        return (f"Kitap Adi : {self.ad} \n"
                f"Yazar : {self.yazar} \n"
                f"Yili : {self.yili} \n"
                f"Dagitim Şirketi : {self.dagitim} \n"
                f"Baski Sayisi : {self.baski} \n"
                f"Eklenilme Tarihi : {self.tarih} \n"
                f"Kütüphanedemi = {'evet' if self.burdami == 1 else 'hayir'} \n" 
                f"Kimde : {'Kütüphanede' if self.kimde == None else self.kimde} \n")
    
class Kutuphane():
    def __init__(self):
        self.baglanti_oldumu = False

    def baglan(self):
        self.baglanti = sqlite3.connect("./veritabani.db")
        self.islem = self.baglanti.cursor()
        self.islem.execute("CREATE TABLE IF NOT EXISTS kitaplar (ad TEXT , yazar TEXT , yili INT , dagitim TEXT , baski INT , tarih TEXT, burdami INT, kimde TEXT)")
        self.baglanti.commit()
        self.baglanti_oldumu = True

        self.logbaglanti = sqlite3.connect("./log.db")
        self.logislem = self.logbaglanti.cursor()
        self.logislem.execute("CREATE TABLE IF NOT EXISTS log (islem TEXT, kitap_ad TEXT, yazar TEXT, yil INT, dagitim TEXT, baski INT, islem_tarihi TEXT, kod INT)")
        self.logbaglanti.commit()


    def baglantikes(self):
        self.islem.close()
        self.baglanti.close()
        self.logislem.close()
        self.logbaglanti.close()
        self.baglanti_oldumu = False
        


    def kitap_ekle(self, kitapbilgileri):
        try:
         eklekitap = kitap(kitapbilgileri[0],kitapbilgileri[1],kitapbilgileri[2],kitapbilgileri[3],kitapbilgileri[4], kitapbilgileri[5],1,None)
         varmi = self.islem.execute("SELECT ad FROM kitaplar WHERE ad = ?",(eklekitap.ad,))
         varmi = varmi.fetchone()
         if (varmi):
             print("Bu kitap zaten eklenmiş.")
         else:
             print("Kitap ekleniyor")
             self.islem.execute("INSERT INTO kitaplar VALUES(?,?,?,?,?,?,?,?)",(eklekitap.ad,eklekitap.yazar,eklekitap.yili,eklekitap.dagitim,eklekitap.baski,eklekitap.tarih,eklekitap.burdami,eklekitap.kimde))
             self.baglanti.commit()
             time.sleep(2)
             islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
             self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{eklekitap.ad} adli kitap eklendi.",eklekitap.ad,eklekitap.yazar,eklekitap.yili,eklekitap.dagitim,eklekitap.baski,islem_tarihi,1))
             self.logbaglanti.commit()
             print("Kitap başariyla eklendi.")
        except:
            print("Kitap eklenirken bir hata oluştu. Lütfen tekrar deneyin.")

    
    def kitap_sorgula(self, deger,neye):
        try:
         ss = f"SELECT * FROM kitaplar WHERE {neye} = ?"
         self.islem.execute(ss,(deger,))
         sonuc = self.islem.fetchall()
         for i in sonuc:
            sorgula = kitap(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
            print(sorgula)
         islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
         self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{deger} adli kitap sorgulandi.",sorgula.ad,sorgula.yazar,sorgula.yili,sorgula.dagitim,sorgula.baski,islem_tarihi,2))
         self.logbaglanti.commit()
         print("Kitap sorgulandi.")
        except:
            print("Kitap bulunamadi")

    
    def kitap_silme(self,deger,neye):
        try:
           sas = f"SELECT * FROM kitaplar WHERE {neye} = ? "
           self.islem.execute(sas,(deger,))
           ssa = self.islem.fetchall()
           if len(ssa) == 0:
               print("Silinecek kitap bulunamadi.")
           else:
              print("Kitap siliniyor")
              time.sleep(2)
              islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
              self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{deger} Veri Tabanindan silindi",ssa[0][0],ssa[0][1],ssa[0][2],ssa[0][3],ssa[0][4],islem_tarihi,3))
              self.logbaglanti.commit()
              ss = f"DELETE FROM kitaplar WHERE {neye} = ? "
              self.islem.execute(ss,(deger,))
              self.baglanti.commit()
              print("Kitap silindi.")
        except:
            print("Degişken adi yanliş girildi. Tekrar deneyin.")
    
    def kitap_guncelle(self, neye,deger, neye2,deger2,neyini, yeni_deger):
        try:
            kontrol = [neye,neye2,neyini]
            if all(x in ["ad", "yazar", "yili", "dagitim", "baski"] for x in kontrol):
             self.islem.execute(f"SELECT * FROM kitaplar WHERE {neye} = ? AND {neye2} = ?", (deger,deger2))
             sonuc = self.islem.fetchall()
             islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
             self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{sonuc[0][0]} adli kitabin {neyini} bilgisi güncellendi.",sonuc[0][0],sonuc[0][1],sonuc[0][2],sonuc[0][3],sonuc[0][4],islem_tarihi,4))
             self.logbaglanti.commit()
             ss = f"UPDATE kitaplar SET {neyini} = ? WHERE {neye} = ? and {neye2} = ?"
             self.islem.execute(ss, (yeni_deger, deger, deger2))
             self.baglanti.commit()
             print("Kitap bilgisi güncellendi.")
            else:
                print("Güncelleme işlemi için geçersiz degişken adi girdiniz. Lütfen tekrar deneyin.")
        except: 
            print("Güncelleme sirasinda bir hata oluştu. Lütfen tekrar deneyin.")
    
    def tum_kitaplari_listele(self):
        try:
            self.islem.execute("SELECT * FROM kitaplar")
            kitaplar = self.islem.fetchall()
            if (kitaplar == []):
                print("Kütüphanede hiç kitap bulunmamaktadir.")
            else:
                for kitapliste in kitaplar:
                    k = kitap(kitapliste[0], kitapliste[1], kitapliste[2], kitapliste[3], kitapliste[4], kitapliste[5], kitapliste[6], kitapliste[7])
                    print(k, "\n")
        except:
            print("Kitaplar listelenirken bir hata oluştu. Lütfen tekrar deneyin.")
    
    def oduncver(self,kitap_ad,kim):
        try:
            self.islem.execute("SELECT * FROM kitaplar WHERE ad = ?",(kitap_ad,))
            kitap = self.islem.fetchall()
            islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
            self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{kitap_ad} adli kitap {kim} kişisine ödünç verildi.",kitap_ad,kitap[0][1],kitap[0][2],kitap[0][3],kitap[0][4],islem_tarihi,5))
            self.logbaglanti.commit()
            self.islem.execute("UPDATE kitaplar SET burdami = ? , kimde = ? WHERE ad = ?",(0,kim,kitap_ad))
            self.baglanti.commit()
            print(f"{kitap_ad} adli kitap {kim} kişisine ödünç verildi.")
        except:
            print("Ödünç verme işlemi sirasinda bir hata oluştu. Lütfen tekrar deneyin.")
    
    def oduncal(self,kitap_ad):
        try:
            self.islem.execute("UPDATE kitaplar SET burdami = ? , kimde = ? WHERE ad = ? ",(1,None,kitap_ad))
            self.baglanti.commit()
            self.islem.execute("SELECT * FROM kitaplar WHERE ad = ?",(kitap_ad,))
            kitap = self.islem.fetchall()
            islem_tarihi = time.strftime("%Y-%m-%d %H:%M:%S")   # Log kaydi için tarih
            self.logislem.execute("INSERT INTO log VALUES(?,?,?,?,?,?,?,?)",(f"{kitap_ad} adli kitap kütüphaneye iade edildi.",kitap_ad,kitap[0][1],kitap[0][2],kitap[0][3],kitap[0][4],islem_tarihi,6))
            self.logbaglanti.commit()
        except:
            print("Ödünç alma işlemi sirasinda bir hata oluştu. Lütfen tekrar deneyin.")

    
    def log_listele(self,nekadar):
        try:
            self.logislem.execute("SELECT * FROM log")
            self.loglar = self.logislem.fetchall()
            for i in range(len(self.loglar)-nekadar, len(self.loglar)):
                print(f"İşlem: {self.loglar[i][0]}, \n Kitap Adı: {self.loglar[i][1]}, \n Yazar: {self.loglar[i][2]}, \n Yıl: {self.loglar[i][3]}, \n Dağıtım: {self.loglar[i][4]}, \nBaskı: {self.loglar[i][5]}, \n İşlem Tarihi: {self.loglar[i][6]}, \n Kod: {self.loglar[i][7]} \n\n")
        except:
            print("Loglar listelenirken bir hata oluştu. Lütfen tekrar deneyin.")
