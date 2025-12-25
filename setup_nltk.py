import nltk

print("Mendownload data NLTK yang diperlukan...")
try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    print("Download selesai!")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")