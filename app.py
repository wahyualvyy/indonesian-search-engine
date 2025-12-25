import streamlit as st
import pandas as pd
import os
from engine import SearchEngine

# Konfigurasi Halaman
st.set_page_config(page_title="Mesin Pencari Berita", page_icon="🔍")

@st.cache_resource
def initialize_engine():
    # Cek apakah model sudah ada supaya tidak training ulang setiap reload
    if os.path.exists('search_engine.pkl'):
        return SearchEngine.load_model('search_engine.pkl')
    else:
        engine = SearchEngine()
        # Pastikan file dataset_berita.csv sudah digenerate
        if os.path.exists('dataset_berita.csv'):
            engine.load_data_and_index("dataset_berita.csv")
            engine.save_model()
            return engine
        else:
            return None

def highlight_text(text, query):
    # Highlight kata dalam query yang muncul di teks (Bonus Feature)
    words = query.lower().split()
    for word in words:
        if len(word) > 2: # Hanya highlight kata > 2 huruf
            # Case insensitive replace dengan HTML mark
            text = text.replace(word, f"<mark style='background-color: yellow;'>{word}</mark>")
            text = text.replace(word.capitalize(), f"<mark style='background-color: yellow;'>{word.capitalize()}</mark>")
    return text

# --- UI Layout ---
st.title("🔍 IndoSearch Engine")
st.markdown("Mesin pencari berita sederhana dengan *TF-IDF* dan *Cosine Similarity*.")

engine = initialize_engine()

if engine is None:
    st.error("File 'dataset_berita.csv' tidak ditemukan. Jalankan 'create_data.py' terlebih dahulu.")
else:
    # Input Query
    query = st.text_input("Masukkan kata kunci pencarian:", placeholder="Contoh: ekonomi inflasi, kesehatan vaksin...")

    if st.button("Cari") or query:
        if query:
            with st.spinner('Mencari dokumen relevan...'):
                results = engine.search(query, top_k=10)

            if results:
                st.success(f"Ditemukan {len(results)} dokumen relevan.")
                
                for i, item in enumerate(results):
                    with st.expander(f"{i+1}. {item['judul']} (Score: {item['score']})"):
                        # Bonus: Highlighting
                        highlighted_content = highlight_text(item['isi'], query)
                        st.markdown(highlighted_content, unsafe_allow_html=True)
                        st.caption(f"Doc ID: {item['id']}")
            else:
                st.warning("Tidak ditemukan dokumen yang cocok.")