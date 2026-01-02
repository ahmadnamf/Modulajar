import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚")

# --- KONFIGURASI API ---
try:
    KEY_NYA = st.secrets["API_KEY"]
    genai.configure(api_key=KEY_NYA)
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# --- TAMPILAN ---
st.title("📚 AI Modul Ajar (Versi Canvas)")
st.write("Susun, Edit, dan Simpan Modul Ajar Anda di sini.")

# Sidebar untuk Input
with st.sidebar:
    st.header("⚙️ Pengaturan Modul")
    jenjang = st.selectbox("Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
    mapel = st.text_input("Mata Pelajaran:", placeholder="Fikih, Biologi, dll")
    topik = st.text_area("Topik Materi:", placeholder="Zakat Fitrah, Sel, dll")
    generate_btn = st.button("✨ Generate Modul")

# Inisialisasi session state untuk menyimpan hasil agar tidak hilang saat edit
if "hasil_modul" not in st.session_state:
    st.session_state.hasil_modul = ""

# Proses Generate
if generate_btn:
    if not mapel or not topik:
        st.warning("Mohon lengkapi Mapel dan Topik di sidebar.")
    else:
        with st.spinner("AI sedang menulis modul..."):
            try:
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                nama_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_list else model_list[0]
                model = genai.GenerativeModel(nama_model)
                
                prompt = f"""
                Anda adalah pakar kurikulum nasional yang menguasai regulasi pendidikan terbaru tahun 2025/2026.
                Tugas Anda adalah menyusun Modul Ajar Kurikulum Merdeka yang SEPENUHNYA PATUH pada:
                1. Permendikdasmen No. 13 Tahun 2025 (Standar Kurikulum Nasional Terbaru).
                2. KMA No. 1503 Tahun 2025 (Pedoman Implementasi Kurikulum pada Madrasah).

                DATA MODUL:
                - Jenjang: {jenjang}
                - Mata Pelajaran: {mapel}
                - Topik: {topik}

                KOMPONEN WAJIB SESUAI REGULASI TERBARU (2025/2026):
                A. IDENTITAS MODUL: (Fase, Kelas, Alokasi Waktu).
                B. TUJUAN PEMBELAJARAN: (Berbasis kompetensi esensial).
                C. PROFIL PELAJAR:
                   - Profil Pelajar Pancasila (P3).
                   - Profil Pelajar Rahmatan Lil Alamin (P2RA) dengan sub-nilai relevan sesuai KMA 1503/2025.
                D. LANGKAH PEMBELAJARAN: (Berdiferensiasi, aktif, dan inovatif).
                E. ASESMEN: (Diagnostik/Awal, Formatif, dan Sumatif).
                F. MEDIA & SUMBER BELAJAR: (Termasuk integrasi literasi digital).

                INSTRUKSI KHUSUS:
                - Pastikan integrasi nilai moderasi beragama dan adab muncul secara eksplisit dalam langkah pembelajaran sesuai spirit KMA 1503/2025.
                - Gunakan format Markdown yang rapi (Heading, List, dan Tabel).
                """
                response = model.generate_content(prompt)
                st.session_state.hasil_modul = response.text
            except Exception as e:
                st.error(f"Error: {e}")

# --- AREA CANVAS (EDITING) ---
if st.session_state.hasil_modul:
    st.markdown("---")
    st.subheader("📝 Edit Modul Ajar")
    st.info("Silakan edit teks di bawah ini jika ada yang ingin disesuaikan.")
    
    # Area Edit (Canvas)
    teks_edit = st.text_area("Konten Modul:", value=st.session_state.hasil_modul, height=500)
    
    # Tombol Aksi di bawah Canvas
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Hasil Edit (.txt)",
            data=teks_edit,
            file_name=f"Modul_{mapel}_{topik}.txt",
            mime="text/plain",
        )
    with col2:
        st.write("💡 *Gunakan Ctrl+A & Ctrl+C untuk copy semua teks.*")
else:
    st.info("Silakan isi data di sebelah kiri dan klik 'Generate' untuk memulai.")

st.markdown("---")
st.caption("Aplikasi Modul Ajar Madrasah Berbasis AI")
