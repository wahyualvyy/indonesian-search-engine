import pandas as pd
import numpy as np
import re
import string
import nltk
import pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory # type: ignore
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Konfigurasi Preprocessing ---
factory = StemmerFactory()
stemmer = factory.create_stemmer()
try:
    list_stopwords = set(stopwords.words('indonesian'))
except:
    nltk.download('stopwords')
    list_stopwords = set(stopwords.words('indonesian'))

class SearchEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.documents = None # DataFrame asli
    
    def preprocessing(self, text):
        """
        Tahapan: Case Folding -> Cleaning -> Tokenization (implicit in stemming loop) -> Stopword Removal -> Stemming
        """
        if not isinstance(text, str):
            return ""
        
        # 1. Case Folding
        text = text.lower()
        
        # 2. Cleaning (Hapus angka dan tanda baca)
        text = re.sub(r"\d+", "", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 3. Stopword Removal & Stemming
        # Sastrawi stemmer cukup lambat, jadi kita split manual untuk stopword dulu
        words = text.split()
        filtered_words = [w for w in words if w not in list_stopwords]
        
        # Gabung kembali dan stem kalimat utuh (Sastrawi lebih akurat context-aware, tapi lambat)
        # Untuk performa, kita stem per kata
        stemmed_words = [stemmer.stem(w) for w in filtered_words]
        
        return " ".join(stemmed_words)

    def load_data_and_index(self, csv_path):
        print("Memuat dataset...")
        self.documents = pd.read_csv(csv_path)
        
        print(f"Melakukan preprocessing pada {len(self.documents)} dokumen. Mohon tunggu...")
        # Gabungkan Judul dan Isi untuk indexing agar pencarian lebih luas
        content_to_index = self.documents['judul'] + " " + self.documents['isi']
        
        # Terapkan preprocessing
        # Note: Ini akan memakan waktu tergantung jumlah dokumen karena Sastrawi
        clean_content = content_to_index.apply(self.preprocessing)
        
        print("Membangun Index TF-IDF...")
        self.tfidf_matrix = self.vectorizer.fit_transform(clean_content)
        print("Indexing selesai!")

    def search(self, query, top_k=10):
        """
        Menerima query -> Preprocessing -> Transform ke Vector -> Hitung Cosine Sim -> Return Top K
        """
        # 1. Preprocess Query
        clean_query = self.preprocessing(query)
        
        # 2. Transform ke Vector
        query_vector = self.vectorizer.transform([clean_query])
        
        # 3. Hitung Cosine Similarity
        # Hasilnya adalah array similarity antara query dan setiap dokumen
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # 4. Ranking
        # Ambil indeks dokumen dengan skor tertinggi
        # argsort mengurutkan dari kecil ke besar, jadi kita ambil dari belakang
        related_docs_indices = similarity_scores.argsort()[::-1]
        
        results = []
        for idx in related_docs_indices[:top_k]:
            score = similarity_scores[idx]
            if score > 0: # Hanya ambil yang relevan (score > 0)
                doc = self.documents.iloc[idx]
                results.append({
                    'id': doc['id'],
                    'judul': doc['judul'],
                    'isi': doc['isi'],
                    'score': round(score, 4)
                })
        
        return results

    def save_model(self, filename='search_engine.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(filename='search_engine.pkl'):
        with open(filename, 'rb') as f:
            return pickle.load(f)

# Testing manual jika dijalankan langsung
if __name__ == "__main__":
    engine = SearchEngine()
    engine.load_data_and_index("dataset_berita.csv")
    res = engine.search("teknologi komputer")
    print(res)