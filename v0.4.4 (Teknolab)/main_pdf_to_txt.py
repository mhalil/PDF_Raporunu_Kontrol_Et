import os, glob
from PyPDF2 import PdfReader
import pandas as pd

##### dosya adini al, veriyi kaydet #####
def pdf_verisini_kaydet():
	pdf_adi = input("PDF dosyasinin adini, uzantisiz olarak yazin: ")
	dosya_adi = str(pdf_adi) + ".pdf"	# Dosya adı ve uzantisi
	pdf_dosyasi = PdfReader(dosya_adi) # Dosya adı ve uzantisi
	toplam_safya_sayisi = len(pdf_dosyasi.pages)

	### Mevcut "pdf_verisi.txt" dosyasını sil
	txt_liste = glob.glob("*.t*")
	print(txt_liste)
	for i in txt_liste:
		os.remove(i)
		print(f"{i} dosyası silindi.")
	################################################

	##### PDF Dosya içeriğini "pdf_verisi.txt" adıyla kaydeden Fonksiyon. ######
	def veriyi_kaydet():
		for sayfa in range(toplam_safya_sayisi):
			with open("pdf_verisi.txt", "a", encoding="utf8") as dosya: 
				dosya.write(pdf_dosyasi.pages[sayfa].extract_text())
	
	veriyi_kaydet()
################################################

##### pdf_to_txt() Fonksiyonunu Çalıştır. ######
# #pdf_verisini_kaydet()
################################################

##### pdf_verisi.txt dosyasını oku, belirtilen ifade ile biten satırları ekrana yazdır.
with open("pdf_verisi.txt", "r", encoding="utf-8") as dosya:
	icerik = dosya.readlines()
	# #print(icerik)
	gecici_numune_adi = ""
	gecici_analiz = ""
	for ic in icerik:
		if "Name, identity" in ic: 
			gecici_numune_adi = ic
		
		elif "Analiz" in ic:
			gecici_analiz = ic
			
		elif "%" in ic or "N/mm^2" in ic or "HBW" in ic or "Shore" in ic:
			
			if "HBW" in ic:
				ic = ic.replace("HBW", " HBW") 
				
			elif "Shore" in ic:
				ic = ic.replace(" Shore", "  Shore") 			
				
			### sonucları "degerler.tsv" adıyla kaydet
			with open("degerler.tsv", "a", encoding="utf-8") as sonuc:
				
				if "Kilit Mekanizması" in gecici_numune_adi and "ParametersAnaliz" in gecici_analiz:	# Gövde Kapak Malzemesi Numunesi ile Kilit Mekanizması Numunesinin Mekanik testlerinin (Rm, Rp0,2,...) isimlerini ayrıştırıp aratmak için düzenleme yapıyorum
					gecici_analiz = "Paslanmaz Celik "
					
				sonuc.write(gecici_numune_adi[37:-1] + "|" + gecici_analiz[:-1] + "|" + ic[:-1] + "|" + ic.split("  ")[0].replace("*", "") + "|" + ic.split("  ")[1].replace(".", ",") + "\n")
				
print("Ayıklanan test sonucları, 'degerler.tsv' dosyasına kaydedildi")

#################################################

baslik = ["Numune", "Analiz Açıklaması", "Analiz Sonucu", "Element / Test",	"Sonuc"]

df_tsv = pd.read_csv("degerler.tsv", sep = "|", header = None, names = baslik)
# #print(df_tsv)

df_tsv["Aranan"] = df_tsv["Analiz Açıklaması"] + "_" + df_tsv["Element / Test"]
# #print(df_tsv)


sartname_degerleri = { 
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_min' : 0.03,	# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_max' : 0.065,	# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_min' : 3.5,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_max' : 3.9,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_min' : 2,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_max' : 3,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_min' : 0.15,	# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_max' : 0.9,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_min' : -1,		# Gövde Kapak Malzemesi	
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_max' : 0.1,		# Gövde Kapak Malzemesi
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_min' : -1,		# Gövde Kapak Malzemesi	
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_max' : 0.03,	# Gövde Kapak Malzemesi
		'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_min' : 170,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_max' : 230,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_min' : 170,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_max' : 230,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_min' : 170,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_max' : 230,				# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_min' : 500,		# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_max' : 1_000_000,	# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_Rp0,2_min' : 320,						# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_Rp0,2_max' : 1_000_000,					# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_A5_min' : 7,							# Gövde ve Kapak Malzemesi
		'ParametersAnaliz Sonuçları_A5_max' : 1_000_000						# Gövde ve Kapak Malzemesi
		}

def min_deger(aranan):
	aranan += "_min"
	if aranan in sartname_degerleri.keys():
		return sartname_degerleri[aranan]

def max_deger(aranan):
	aranan += "_max"
	if aranan in sartname_degerleri.keys():
		return sartname_degerleri[aranan]

### Şartname değerlerini Tabloya ekle
df_tsv["Min."] = df_tsv["Aranan"].apply(min_deger)
df_tsv["Max."] = df_tsv["Aranan"].apply(max_deger)
print(df_tsv)

### Sonucu KAYDET
# #df_tsv.to_excel("dnm.xlsx")
#####################################
