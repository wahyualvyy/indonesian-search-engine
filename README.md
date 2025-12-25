# 🔍 Indonesian News Search Engine

````markdown
# 🔍 Indonesian News Search Engine

**Mesin Pencari Berita Indonesia** sederhana yang dibangun menggunakan Python. Sistem ini menerapkan metode _Information Retrieval_ klasik seperti **TF-IDF** untuk pembobotan kata dan **Cosine Similarity** untuk peranking dokumen.

Dilengkapi dengan antarmuka web interaktif menggunakan **Streamlit** dan fitur _scraping_ data otomatis via RSS Feed.

---

## 📋 Fitur Utama

- **Preprocessing Lengkap:**
  - Case Folding & Cleaning (Regex).
  - Tokenization.
  - Stopword Removal (NLTK Indonesian).
  - Stemming (Sastrawi) untuk mengembalikan kata ke bentuk dasar.
- **Indexing & Retrieval:**
  - Menggunakan **TF-IDF Vectorizer** (Scikit-Learn).
  - Perhitungan relevansi menggunakan **Cosine Similarity**.
  - Penyimpanan model index menggunakan `pickle` untuk performa cepat.
- **Dataset Generator:**
  - Mengambil data _real-time_ dari RSS Feed (Antara News & Republika).
  - Mekanisme _fallback_ otomatis (Full text vs Summary) agar anti-blokir.
- **Antarmuka Pengguna (GUI):**
  - Web-based interface dengan **Streamlit**.
  - **Highlighting**: Menandai kata kunci pencarian dengan warna kuning pada hasil.
- **Evaluasi Sistem:**
  - Menghitung Precision@5, Precision@10, dan Mean Average Precision (MAP).

---

## 🛠️ Instalasi & Persiapan

Pastikan Anda sudah menginstal **Python 3.8+** di komputer Anda.

1.  **Install Library**
    Jalankan perintah berikut di terminal untuk menginstal semua ketergantungan:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Download Data NLTK**
    Jalankan skrip setup untuk mengunduh kamus _stopwords_ dan _tokenizer_:
    ```bash
    python setup_nltk.py
    ```

---

## 🚀 Cara Penggunaan

Ikuti langkah-langkah ini secara berurutan:

### 1. Generate Dataset (Crawling Data)

Langkah ini akan mengambil berita terbaru dari internet dan menyimpannya ke `dataset_berita.csv`.

```bash
python create_data.py
```
````

> _Tunggu hingga muncul pesan "SUKSES"._

### 2. Jalankan Aplikasi Web

Buka antarmuka mesin pencari di browser.

```bash
python -m streamlit run app.py

```

_Aplikasi akan terbuka otomatis di http://localhost:8501_

### 3. Evaluasi Performa (Opsional)

Untuk melihat nilai akurasi (Precision & MAP) berdasarkan 20 query pengujian.

```bash
python evaluation.py

```

---

## 📂 Struktur File

Berikut adalah penjelasan fungsi dari setiap file dalam proyek ini:

| Nama File            | Deskripsi                                                                    |
| -------------------- | ---------------------------------------------------------------------------- |
| `app.py`             | **Main Program**. Interface web menggunakan Streamlit.                       |
| `engine.py`          | **Core Logic**. Berisi class `SearchEngine` (Preprocessing, TF-IDF, Search). |
| `create_data.py`     | Script untuk mengambil data berita via RSS Feed (Antara/Republika).          |
| `evaluation.py`      | Script untuk menghitung metrik evaluasi (MAP, P@5, P@10).                    |
| `setup_nltk.py`      | Script inisialisasi untuk download data NLTK.                                |
| `requirements.txt`   | Daftar library yang dibutuhkan.                                              |
| `dataset_berita.csv` | File database berita (dihasilkan oleh `create_data.py`).                     |
| `search_engine.pkl`  | File model index yang disimpan (dihasilkan otomatis oleh `app.py`).          |

---

## 📊 Metrik Evaluasi

Proyek ini menggunakan metode evaluasi standar IR:

- **Precision@K:** Mengukur proporsi dokumen relevan dalam K hasil teratas.
- **MAP (Mean Average Precision):** Rata-rata dari skor presisi rata-rata (AP) untuk sekumpulan query, memberikan gambaran performa ranking secara keseluruhan.

---

## 👥 Kredit

**Tugas Search Engine - Kelompok [Masukkan Nomor Kelompok]**

- Anggota 1: [Mochammad Wahyu Alvy Kusuma]
- Anggota 2: [Luluk Asti Qomariah]
- Anggota 3: [M. Hafizh Fattah]

---

_Dibuat untuk memenuhi tugas Mata Kuliah Web & Text Mining._

```

```
