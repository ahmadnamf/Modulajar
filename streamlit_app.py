import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚")

# --- 2. KONFIGURASI API KEY ---
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ API_KEY tidak ditemukan di Secrets Streamlit Cloud!")
    st.stop()

# --- 3. TAMPILAN HEADER ---
st.title("📚 AI Modul Ajar Madrasah")
st.write("Sesuai **Permendikdasmen 13/2025** & **KMA 1503/2025**")

# --- 4. BAGIAN INFORMASI UMUM (PASTI MUNCUL DI ATAS) ---
st.subheader("📋 Informasi Umum")
col1, col2 = st.columns(2)
with col1:
    nama_guru = st.text_input("Nama Guru:", placeholder="Contoh: Ahmad Fauzi, S.Pd.I")
    nama_madrasah = st.text_input("Nama Madrasah:", placeholder="Contoh: MTs Negeri 1")
with col2:
    tahun_ajaran = st.text_input("Tahun Ajaran:", value="2025/2026")
    alokasi_waktu = st.text_input("Alokasi Waktu:", placeholder="Contoh: 2 JP (2 x 40 menit)")

# --- 5. DETAIL MATERI ---
st.subheader("📖 Detail Materi")
jenjang = st.selectbox("Jenjang/Fase:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Aqidah Akhlak, Biologi")
topik = st.text_area("Topik/Bab:", placeholder="Contoh: Pengurusan Jenazah")

generate_btn = st.button("✨ SUSUN MODUL AJAR")

# Simpan hasil di session state agar tidak hilang saat refresh kecil
if "hasil_modul" not in st.session_state:
    st.session_state.hasil_modul = ""

# --- 6. LOGIKA GENERATE (PERBAIKAN ERROR 404) ---
if generate_btn:
    if not mapel or not topik:
        st.warning("Mohon isi Mata Pelajaran dan Topik!")
    else:
        with st.spinner("⏳ Menghubungkan ke AI..."):
            try:
                # Mencari model yang tersedia secara dinamis agar tidak error 404
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # Prioritaskan gemini-1.5-flash, jika tidak ada pakai yang tersedia
                model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
                
                model = genai.GenerativeModel(model_name)
                
                prompt = f"""
                Buatlah Modul Ajar Kurikulum Merdeka 2025/2026.
                
                IDENTITAS (WAJIB TAMPILKAN DALAM TABEL):
                Guru: {nama_guru}, Madrasah: {nama_madrasah}, Tahun: {tahun_ajaran}, Mapel: {mapel}, Jenjang: {jenjang}, Waktu: {alokasi_waktu}, Topik: {topik}.

                STRUKTUR ISI:
                1. TUJUAN PEMBELAJARAN.
                2. PROFIL PELAJAR P3 & P2RA (Sesuai KMA 1503/2025).
                3. LANGKAH PEMBELAJARAN (Pendahuluan, Inti, Penutup).
                4. ASESMEN.

                PENTING: Gunakan format Markdown. # untuk Judul, **teks** untuk tebal. 
                Sajikan bagian Identitas dan Asesmen dalam bentuk TABEL.
                """
                
                response = model.generate_content(prompt)
                st.session_state.hasil_modul = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# --- 7. TAMPILAN HASIL (TEBAL, MIRING, TABEL) ---
if st.session_state.hasil_modul:
    st.markdown("---")
    tab_rapi, tab_edit = st.tabs(["✨ HASIL RAPI (SIAP COPAS)", "📝 EDIT TEKS"])
    
    with tab_rapi:
        # st.markdown akan merender Tebal dan Tabel secara otomatis
        st.markdown(st.session_state.hasil_modul)
        st.info("💡 **Cara Copy:** Sorot teks di atas, klik kanan Copy, lalu Paste ke Word.")

    with tab_edit:
        st.session_state.hasil_modul = st.text_area("Editor:", value=st.session_state.hasil_modul, height=500)

    if st.button("🗑️ Hapus & Buat Baru"):
        st.session_state.hasil_modul = ""
        st.rerun()

st.markdown("---")
st.caption("Aplikasi Modul Ajar - Update Regulasi 2025/2026")
