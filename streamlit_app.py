import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Super AI Guru Madrasah", page_icon="🎓", layout="centered")

# --- 2. KONFIGURASI API KEY ---
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ API_KEY tidak ditemukan di Secrets!")
    st.stop()

# --- 3. TAMPILAN HEADER ---
st.title("🎓 Super AI Guru Madrasah")
st.write("Perangkat Administrasi Lengkap: **Permendikdasmen 13/2025** & **KMA 1503/2025**")

# --- 4. INFORMASI UMUM ---
with st.container():
    st.subheader("📋 Informasi Umum")
    col1, col2 = st.columns(2)
    with col1:
        nama_guru = st.text_input("Nama Guru:", placeholder="Contoh: Ahmad Fauzi, S.Pd.I")
        nama_madrasah = st.text_input("Nama Madrasah:", placeholder="Contoh: MTs Negeri 1")
    with col2:
        tahun_ajaran = st.text_input("Tahun Ajaran:", value="2025/2026")
        alokasi_waktu = st.text_input("Alokasi Waktu:", placeholder="Contoh: 2 JP")

# --- 5. PILIHAN JENIS DOKUMEN (FITUR BARU) ---
st.markdown("---")
st.subheader("🛠️ Pilih Perangkat yang Ingin Dibuat")
jenis_dokumen = st.selectbox(
    "Pilih Jenis Dokumen:", 
    [
        "Modul Ajar (Lengkap)", 
        "Alur Tujuan Pembelajaran (ATP)", 
        "Program Semester (Promes)", 
        "Modul Proyek P5RA", 
        "Instrumen Asesmen (Soal & Rubrik)",
        "Jurnal Refleksi Guru"
    ]
)

col_mapel, col_fase = st.columns([2, 1])
with col_mapel:
    mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih")
with col_fase:
    jenjang = st.selectbox("Fase:", ["Fase D (MTs)", "Fase E (MA 10)", "Fase F (MA 11-12)"])

topik = st.text_area("Topik/Materi Utama:", placeholder="Contoh: Thaharah, Ekonomi Syariah, dll")

generate_btn = st.button(f"✨ Buat {jenis_dokumen} Sekarang")

if "hasil_dokumen" not in st.session_state:
    st.session_state.hasil_dokumen = ""

# --- 6. LOGIKA GENERATE ---
if generate_btn:
    if not mapel or not topik:
        st.warning("Mohon lengkapi Mata Pelajaran dan Topik!")
    else:
        with st.spinner(f"⏳ Sedang menyusun {jenis_dokumen}..."):
            try:
                # Perbaikan Error 404: Auto-detect model
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""
                Bertindaklah sebagai Pakar Kurikulum Madrasah. Buatlah dokumen '{jenis_dokumen}' sesuai regulasi Permendikdasmen 13/2025 dan KMA 1503/2025.
                
                IDENTITAS:
                Guru: {nama_guru}, Madrasah: {nama_madrasah}, Tahun: {tahun_ajaran}, Mapel: {mapel}, Jenjang: {jenjang}, Waktu: {alokasi_waktu}, Topik: {topik}.

                INSTRUKSI KHUSUS UNTUK {jenis_dokumen}:
                - Jika Modul Ajar: Sertakan langkah pembelajaran dan P2RA.
                - Jika ATP: Buat urutan TP yang logis dari awal ke akhir.
                - Jika P5RA: Fokus pada nilai moderasi beragama dan profil rahmatan lil alamin.
                - Jika Asesmen: Sertakan soal HOTS dan kunci jawaban serta rubrik.
                
                FORMAT: Gunakan Markdown yang rapi, buat TABEL untuk data yang bersifat matriks. JANGAN gunakan banyak simbol bintang.
                """
                
                response = model.generate_content(prompt)
                st.session_state.hasil_dokumen = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- 7. TAMPILAN HASIL ---
if st.session_state.hasil_dokumen:
    st.markdown("---")
    tab1, tab2 = st.tabs(["✨ HASIL RAPI", "📝 EDITOR"])
    
    with tab1:
        st.markdown(st.session_state.hasil_dokumen)
        st.success(f"✅ {jenis_dokumen} berhasil dibuat! Silakan Copy ke Word.")

    with tab2:
        st.session_state.hasil_dokumen = st.text_area("Edit konten:", value=st.session_state.hasil_dokumen, height=500)

    if st.button("🗑️ Hapus & Buat Baru"):
        st.session_state.hasil_dokumen = ""
        st.rerun()

st.markdown("---")
st.caption("Super AI Guru Madrasah - Update 2026")
