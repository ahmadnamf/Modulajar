import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚", layout="centered")

# --- 2. KONFIGURASI API KEY ---
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ API Key tidak ditemukan! Masukkan API_KEY di menu Secrets Streamlit Cloud.")
    st.stop()

# --- 3. TAMPILAN HEADER ---
st.title("📚 AI Modul Ajar Madrasah")
st.write("Berbasis **Permendikdasmen No. 13/2025** & **KMA No. 1503/2025**")

# --- 4. INPUT INFORMASI UMUM ---
with st.expander("📝 ISI INFORMASI UMUM (KLIK DISINI)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nama_guru = st.text_input("Nama Guru:", "Ahmad Fauzi, S.Pd.I")
        nama_madrasah = st.text_input("Nama Madrasah:", "MTs Negeri 1")
    with col2:
        tahun_ajaran = st.text_input("Tahun Ajaran:", "2025/2026")
        alokasi_waktu = st.text_input("Alokasi Waktu:", "2 x 40 Menit")

# --- 5. INPUT DETAIL MATERI ---
st.subheader("📖 Detail Materi")
jenjang = st.selectbox("Pilih Jenjang/Fase:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")
topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Zakat Fitrah, Pembelahan Sel, dll")

generate_btn = st.button("✨ GENERATE MODUL AJAR")

# --- 6. LOGIKA GENERATE ---
if "hasil_modul" not in st.session_state:
    st.session_state.hasil_modul = ""

if generate_btn:
    if not mapel or not topik:
        st.warning("Silakan isi Mata Pelajaran dan Topik terlebih dahulu!")
    else:
        with st.spinner("⏳ Sedang memproses modul sesuai aturan terbaru..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Buatlah Modul Ajar Kurikulum Merdeka terbaru 2025/2026.
                
                IDENTITAS (Sajikan dalam bentuk TABEL di awal):
                Nama Guru: {nama_guru}, Madrasah: {nama_madrasah}, Tahun: {tahun_ajaran}, Mapel: {mapel}, Jenjang: {jenjang}, Waktu: {alokasi_waktu}, Topik: {topik}.

                STRUKTUR WAJIB:
                1. Kompetensi Awal & Tujuan Pembelajaran.
                2. Profil Pelajar Pancasila & Rahmatan Lil Alamin (P2RA) sesuai KMA 1503/2025.
                3. Langkah Pembelajaran (Pendahuluan, Inti, Penutup).
                4. Asesmen (Awal, Formatif, Sumatif).
                
                FORMAT TAMPILAN:
                - Gunakan Bold (Tebal) untuk judul bagian.
                - Gunakan TABEL Markdown untuk Identitas dan Asesmen.
                - JANGAN gunakan bintang double (**) jika tidak perlu, pastikan tampilan bersih.
                """
                
                response = model.generate_content(prompt)
                st.session_state.hasil_modul = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# --- 7. TAMPILAN HASIL (TEBAL, MIRING, TABEL) ---
if st.session_state.hasil_modul:
    st.markdown("---")
    
    # Gunakan Tabs agar user bisa memilih tampilan
    tab_rapi, tab_edit = st.tabs(["✨ HASIL SIAP COPAS", "✍️ EDITOR TEKS"])
    
    with tab_rapi:
        st.success("Berhasil! Silakan blok teks di bawah ini dan Copy ke Word.")
        # st.markdown adalah kunci agar Tebal, Miring, dan Tabel muncul otomatis
        st.markdown(st.session_state.hasil_modul)

    with tab_edit:
        st.session_state.hasil_modul = st.text_area("Edit manual jika perlu:", value=st.session_state.hasil_modul, height=500)

    # Tombol Download & Hapus
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Download File .txt", st.session_state.hasil_modul, f"Modul_{mapel}.txt")
    with c2:
        if st.button("🗑️ Buat Baru"):
            st.session_state.hasil_modul = ""
            st.rerun()

st.markdown("---")
st.caption("Aplikasi Modul Ajar - Regulasi 2025")
