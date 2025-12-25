import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# Daftar URL RSS Feed (Sumber Data Stabil)
rss_urls = [
    "https://www.antaranews.com/rss/terkini.xml",
    "https://www.antaranews.com/rss/top-news.xml",
    "https://www.antaranews.com/rss/ekonomi.xml",
    "https://www.antaranews.com/rss/dunia.xml",
    "https://www.republika.co.id/rss",
    "https://www.republika.co.id/rss/news/nasional",
    "https://www.republika.co.id/rss/news/internasional"
]

def get_rss_data(limit=100):
    data = []
    seen_titles = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"🔄 Memulai pengambilan data via RSS Feed (Target: {limit})...")
    print("---------------------------------------------------------")

    for rss_url in rss_urls:
        if len(data) >= limit:
            break
            
        try:
            print(f"📡 Membaca Feed: {rss_url}...")
            response = requests.get(rss_url, headers=headers, timeout=10)
            
            # Parsing XML
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            print(f"   -> Ditemukan {len(items)} artikel di feed ini.")
            
            for item in items:
                if len(data) >= limit:
                    break
                
                title = item.title.text.strip()
                link = item.link.text.strip()
                
                # Gunakan description sebagai cadangan konten jika gagal masuk ke link
                description = item.description.text.strip() if item.description else ""
                
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                
                # --- Tahap 2: Ambil Isi Full dari Link ---
                try:
                    # Delay sangat singkat karena RSS server biasanya lebih toleran
                    time.sleep(0.2)
                    
                    article_resp = requests.get(link, headers=headers, timeout=5)
                    article_soup = BeautifulSoup(article_resp.text, 'html.parser')
                    
                    full_text = ""
                    
                    # Logika ekstraksi konten berdasarkan situs
                    if "antaranews.com" in link:
                        content_div = article_soup.find('div', class_='post-content')
                        if content_div:
                            # Hapus sampah
                            for bad in content_div(['script', 'style', 'div', 'iframe']):
                                bad.decompose()
                            full_text = content_div.get_text(separator=' ', strip=True)
                            
                    elif "republika.co.id" in link:
                        content_div = article_soup.find('div', class_='article-content')
                        if content_div:
                            full_text = content_div.get_text(separator=' ', strip=True)
                    
                    # --- FALLBACK ---
                    # Jika gagal ambil full text (karena struktur berubah), 
                    # KITA PAKAI DESKRIPSI DARI RSS SAJA.
                    # Ini menjamin data TIDAK KOSONG.
                    if len(full_text) < 50:
                        # Bersihkan tag HTML dari deskripsi RSS
                        desc_soup = BeautifulSoup(description, "html.parser")
                        full_text = desc_soup.get_text(separator=' ', strip=True)
                        print(f"   ⚠️ Menggunakan teks summary untuk: {title[:30]}...")
                    else:
                        print(f"   ✅ Full Text OK: {title[:30]}...")

                    # Simpan data
                    if len(full_text) > 30: # Minimal ada isinya
                        doc_id = len(data) + 1
                        data.append([doc_id, title, full_text])
                        
                except Exception as e:
                    # Jika error koneksi ke link, tetap simpan judul + deskripsi RSS
                    # Agar data tetap bertambah
                    print(f"   ⚠️ Error link, simpan summary saja.")
                    doc_id = len(data) + 1
                    desc_clean = BeautifulSoup(description, "html.parser").get_text()
                    data.append([doc_id, title, desc_clean])

        except Exception as e:
            print(f"❌ Gagal membaca feed {rss_url}: {e}")
            continue

    return data

if __name__ == "__main__":
    berita = get_rss_data(limit=100)
    
    if berita:
        df = pd.DataFrame(berita, columns=["id", "judul", "isi"])
        df.to_csv("dataset_berita.csv", index=False, encoding='utf-8')
        print("\n" + "="*50)
        print(f"🎉 SUKSES! Berhasil menyimpan {len(df)} artikel.")
        print("Dataset siap digunakan. Jalankan 'streamlit run app.py'")
        print("="*50)
    else:
        print("❌ Masih gagal. Sepertinya IP Anda diblokir sementara.")
        print("Solusi: Gunakan tethering HP (beda jaringan) atau gunakan Data Dummy.")