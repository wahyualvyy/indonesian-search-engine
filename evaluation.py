from engine import SearchEngine
import numpy as np

# Inisialisasi Engine
engine = SearchEngine()
# Kita asumsikan engine sudah ditraining atau load dari pickle
try:
    engine = SearchEngine.load_model('search_engine.pkl')
except:
    print("Harap jalankan app.py atau engine.py dulu untuk membuat index.")
    exit()

# --- SETUP GROUND TRUTH ---
# Format: { "query": [list_id_dokumen_relevan] }
# Karena dataset kita random, kita harus membuat asumsi manual atau cek manual.
# Di sini kita buat simulasi logika relevansi berdasarkan keyword generator tadi.
# Contoh: Jika query "saham", dokumen relevan adalah yang genrenya Ekonomi.

df = engine.documents

def get_ground_truth_ids(keyword):
    # Fungsi bantu untuk mencari ID dokumen yang mengandung keyword (sebagai simulasi ground truth)
    return df[df['isi'].str.contains(keyword, case=False)]['id'].tolist()

test_queries = {
    "investasi saham": get_ground_truth_ids("saham"),
    "rumah sakit": get_ground_truth_ids("rumah sakit"),
    "pertandingan bola": get_ground_truth_ids("bola"),
    "pemilu presiden": get_ground_truth_ids("presiden"),
    "teknologi ai": get_ground_truth_ids("AI"),
}

# --- FUNGSI METRIK ---
def calculate_precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = [doc_id for doc_id in retrieved_k if doc_id in relevant_ids]
    return len(relevant_retrieved) / k

def calculate_average_precision(retrieved_ids, relevant_ids):
    precisions = []
    relevant_count = 0
    for i, doc_id in enumerate(retrieved_ids):
        if doc_id in relevant_ids:
            relevant_count += 1
            p_at_i = relevant_count / (i + 1)
            precisions.append(p_at_i)
    
    if not precisions:
        return 0.0
    return sum(precisions) / len(relevant_ids) # Definisi standar AP

# --- JALANKAN EVALUASI ---
print(f"{'Query':<20} | {'P@5':<10} | {'P@10':<10} | {'AP':<10}")
print("-" * 60)

ap_scores = []
p5_scores = []
p10_scores = []

for query_text, relevant_ids in test_queries.items():
    # Search
    results = engine.search(query_text, top_k=20)
    retrieved_ids = [r['id'] for r in results]
    
    # Hitung Metrik
    p5 = calculate_precision_at_k(retrieved_ids, relevant_ids, 5)
    p10 = calculate_precision_at_k(retrieved_ids, relevant_ids, 10)
    ap = calculate_average_precision(retrieved_ids, relevant_ids)
    
    ap_scores.append(ap)
    p5_scores.append(p5)
    p10_scores.append(p10)
    
    print(f"{query_text:<20} | {p5:.4f}     | {p10:.4f}     | {ap:.4f}")

print("-" * 60)
print(f"Mean Average Precision (MAP): {np.mean(ap_scores):.4f}")
print(f"Average P@5: {np.mean(p5_scores):.4f}")