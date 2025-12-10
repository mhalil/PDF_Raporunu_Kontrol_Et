import os, glob
from PyPDF2 import PdfReader
import pandas as pd

##### Çıktılar bütün tablo olarak gösterilsin #########
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
#######################################################
	
##### dosya adini al, veriyi kaydet #########################################################################################
def pdf_verisini_kaydet():
	pdf_adi = input("PDF dosyasinin adini, uzantisiz olarak yazin: ")
	dosya_adi = str(pdf_adi) + ".pdf"	# Dosya adı ve uzantisi
	pdf_dosyasi = PdfReader(dosya_adi) # Dosya adı ve uzantisi
	toplam_safya_sayisi = len(pdf_dosyasi.pages)

	### Mevcut "pdf_verisi_parsel.txt" dosyasını sil
	txt_liste = glob.glob("*.t*")
	# #print(txt_liste)
	for i in txt_liste:
		os.remove(i)
		# #print(f"{i} dosyası silindi.")
	################################################

	##### PDF Dosya içeriğini "pdf_verisi_parsel.txt" adıyla kaydeden Fonksiyon. ######
	def veriyi_kaydet():
		for sayfa in range(toplam_safya_sayisi):
			with open("pdf_verisi_parsel.txt", "a", encoding="utf8") as dosya: 
				dosya.write(pdf_dosyasi.pages[sayfa].extract_text())
	
	veriyi_kaydet()
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

##### pdf_verisini_kaydet() Fonksiyonunu Çalıştır. ##############
pdf_verisini_kaydet()
#############################################################################################################################

##### pdf_verisi_parsel.txt dosyasını oku, belirtilen ifade ile biten satırları "degerler_parsel.tsv" dosyasına yaz. ######################
def TSV_Kaydet():
	with open("pdf_verisi_parsel.txt", "r", encoding="utf-8") as dosya:
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
					
				### sonucları "degerler_parsel.tsv" adıyla kaydet
				with open("degerler_parsel.tsv", "a", encoding="utf-8") as sonuc:
					
					if "Kilit Mekanizması" in gecici_numune_adi and "ParametersAnaliz" in gecici_analiz:	# Gövde Kapak Malzemesi Numunesi ile Kilit Mekanizması Numunesinin Mekanik testlerinin (Rm, Rp0,2,...) isimlerini ayrıştırıp aratmak için düzenleme yapıyorum
						gecici_analiz = "Paslanmaz Celik "
						
					sonuc.write(gecici_numune_adi[37:-1] + "|" + gecici_analiz[:-1] + "|" + ic[:-1] + "|" + ic.split("  ")[0].replace("*", "") + "|" + ic.split("  ")[1].strip() + "\n")
					
	print("Ayıklanan test sonucları, 'degerler_parsel.tsv' dosyasına kaydedildi")
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

##### TSV_Kaydet() Fonksiyonunu Çalıştır. #######################
TSV_Kaydet()
#############################################################################################################################

##### "degerler_parsel.tsv" dosyasından DF olustur ve duzenle. ###############################
baslik = ["Numune", "Analiz Açıklaması", "Analiz Sonucu", "Element / Test",	"Sonuc"]
df_tsv = pd.read_csv("degerler_parsel.tsv", sep = "|", header = None, names = baslik)

df_tsv["Sonuc"] = df_tsv["Sonuc"].replace("Kalan", -1)
df_tsv["Sonuc"] = df_tsv["Sonuc"].replace(to_replace="<", value="", regex=True)
df_tsv["Sonuc"] = df_tsv["Sonuc"].astype('float64')
df_tsv["Aranan"] = df_tsv["Analiz Açıklaması"] + "_" + df_tsv["Element / Test"]
#######################################################################################

sartname_degerleri = { 
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_min' : 0.03,	# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mg_max' : 0.065,	# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_min' : 3.5,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_C_max' : 3.9,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_min' : 2.0,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Si_max' : 3.0,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_min' : 0.15,	# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_Mn_max' : 0.9,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_min' : -1.0,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_P_max' : 0.1,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_S_min' : -1.0,		# Gövde Kapak Malzemesi	- Muayene ve Parsel B.K.
		'Dökme Demir Spektrometrik Analiz (Cast Iron Spectrometric Analysis)_S_max' : 0.03,		# Gövde Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_min' : 170.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_1.Ölçüm Brinell_max' : 230.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_min' : 170.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_2.Ölçüm Brinell_max' : 230.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_min' : 170.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_3.Ölçüm Brinell_max' : 230.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_min' : 500.0,			# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_Çekme Gerilmesi (Rm)_max' : 1_000_000.0,	# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_Rp0,2_min' : 320.0,							# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_Rp0,2_max' : 1_000_000.0,					# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_A5_min' : 7.0,								# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_A5_max' : 1_000_000.0,						# Gövde ve Kapak Malzemesi - Muayene ve Parsel B.K.
		'Paslanmaz Celik_Çekme Gerilmesi (Rm)_min' : 700.0,						# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Celik_Çekme Gerilmesi (Rm)_max' : 1_000_000.0,				# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Celik_Rp0,2_min' : 450.0,									# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Celik_Rp0,2_max' : 1_000_000.0,								# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Celik_A5_min' : 40.0,										# Kilit Mekanizması - A5 Uzama Yüzdesi - Muayene ve Parsel B.K.
		'Paslanmaz Celik_A5_max' : 1_000_000.0,									# Kilit Mekanizması - A5 Uzama Yüzdesi - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_C_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_C_max' : 0.1,						# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Si_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Si_max' : 1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Mn_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Mn_max' : 2.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_P_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_P_max' : 0.05,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_S_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_S_max' : 0.03,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Cr_min' : 15.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Cr_max' : 20.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Ni_min' : 8.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Ni_max' : 19.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Cu_min' : -1.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'Paslanmaz Çelik Spektrometrik Analiz_Cu_max' : 4.0,					# Kilit Mekanizması, Anahtar ve Mafsal Pimi Numuneleri - A2 _ 70 - Muayene ve Parsel B.K.
		'ParametersAnaliz Sonuçları_Kopma Mukavemeti_min' : 9.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Kopma Mukavemeti_max' : 1_000_000.0,		# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Uzama_min' : 300.0,							# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Uzama_max' : 1_000_000.0,					# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 1.Ölçüm_min' : 65.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 1.Ölçüm_max' : 75.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 2.Ölçüm_min' : 65.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 2.Ölçüm_max' : 75.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 3.Ölçüm_min' : 65.0,				# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		'ParametersAnaliz Sonuçları_Shore A 3.Ölçüm_max' : 75.0					# Lastik Conta Malzemesi (EPDM Conta) - Parsel Baca Kapağı
		}

##### Şartnamede belirtilen Min. ve Max. değerlerini, sözlükten bulan fonksiyonlar ###
def min_deger(aranan):
	aranan += "_min"
	if aranan in sartname_degerleri.keys():
		return sartname_degerleri[aranan]

def max_deger(aranan):
	aranan += "_max"
	if aranan in sartname_degerleri.keys():
		return sartname_degerleri[aranan]

def min_kontrol(df):	# Gemini fonksiyonu
    if pd.isna(df['Min.']):
        return "" 
    
    if df['Sonuc'] >= df['Min.']:
        return 'Uygun' 
    else:
        return 'UYGUN DEĞİL'

def max_kontrol(df):	# Gemini fonksiyonu
    if pd.isna(df['Max.']):
        return "" 

    if df['Sonuc'] <= df['Max.']:
        return 'Uygun' 
    else:
        return 'UYGUN DEĞİL'

### Şartname değerlerini Tabloya ekle ################################
df_tsv["Min."] = df_tsv["Aranan"].apply(min_deger)
df_tsv["Max."] = df_tsv["Aranan"].apply(max_deger)

df_tsv['Min.Kontrol'] = df_tsv.apply(min_kontrol, axis=1)
df_tsv['Max.Kontrol'] = df_tsv.apply(max_kontrol, axis=1)

df_tsv.drop("Aranan", axis = 1, inplace = True)		# "Aranan" sütununu sil.

### Sonucu KAYDET
df_tsv.to_excel("Sonuc_ve_Mukayese_Parsel.xlsx")
print("'Sonuc_ve_Mukayese_Parsel.xlsx' dosyası olusturuldu.")
######################################################################
