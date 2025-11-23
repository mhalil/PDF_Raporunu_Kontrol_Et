import os, glob
from PyPDF2 import PdfReader
import pandas as pd

##### dosya adini al, veriyi kaydet #####
def pdf_dosya_adi():
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
pdf_dosya_adi()
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
		
		### Alternatif elif koşulu
		# #elif "Analiz" in ic or "ASTM E1999" in ic or "ASTM E1086" in ic or "EN ISO 6892-1 Metod B" in ic or "Brinell" in ic or "EN ISO 6506-1" in ic or "Shore A  TS ISO 48-2" in ic or "TS ISO 37" in ic:
		
		elif "Analiz" in ic:
			gecici_analiz = ic
			
		elif "%" in ic or "N/mm^2" in ic or "HBW" in ic or "Shore" in ic:
			# ## Sonucları Ekrana yazdır
			# #print(gecici_numune_adi[37:-1], "|", gecici_analiz[:-1], "|", ic[:-1], "|", ic.split("  ")[0].replace("*", ""), "|", ic.split("  ")[1].replace(".", ","), "\n")
			
			if "HBW" in ic:
				ic = ic.replace("HBW", " HBW") 
				
			elif "Shore" in ic:
				ic = ic.replace(" Shore", "  Shore") 			

			### sonucları "sonuc.tsv" adıyla kaydet
			with open("degerler.tsv", "a", encoding="utf-8") as sonuc:
				sonuc.write(gecici_numune_adi[37:-1] + "|" + gecici_analiz[:-1] + "|" + ic[:-1] + "|" + ic.split("  ")[0].replace("*", "") + "|" + ic.split("  ")[1].replace(".", ",") + "\n")
				
print("Ayıklanan test sonucları, 'degerler.tsv' dosyasına kaydedildi")

# #################################################


baslik = ["Malzeme", "Test", "Sonuc", "Element / Test",	"Deger"]

df_tsv = pd.read_csv("degerler.tsv", sep = "|", header = None, names = baslik)
print(df_tsv)

df_tsv["Aranan"] = df_tsv["Test"] + "_" + df_tsv["Element / Test"]
print(df_tsv)

df_tsv.to_excel("dnm.xlsx")


# #sartname_degerleri = { 
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_min' : 0.03,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_max' : 0.065,
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_min' : 3.5,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_max' : 3.9,
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_min' : 2,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_max' : 3,
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_min' : 0.15,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_max' : 0.9,
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_min' : -1,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_max' : 0.1,
					# #'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_min' : -1,	'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_max' : 0.03,
					# #'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_min' : 170,	'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_max' : 230,
					# #'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_min' : 170,	'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_max' : 230,
					# #'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_min' : 170,	'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_max' : 230,
					# #'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_min' : 500,	
					# #'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_max' : 1_000_000,
					# #'ParametersAnaliz Sonuçları_Rp0,2_min' : 320,	
					# #'ParametersAnaliz Sonuçları_Rp0,2_max' : 1_000_000,
					# #'ParametersAnaliz Sonuçları_A5_min' : 7,	
					# #'ParametersAnaliz Sonuçları_A5_max' : 1_000_000					

# #}

# #def kontrol(deger):
	# #pass
