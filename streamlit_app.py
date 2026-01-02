import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚")

# --- KONFIGURASI API ---
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# --- TAMPILAN UTAMA ---
st.title("📚 AI Modul Ajar (Versi Regulasi 2025)")
st.write("Sesuai Permendikdasmen No. 13 Th 2025 & KMA No. 1503 Th 2025")

# --- BAGIAN INFORMASI UMUM ---
st.subheader("📋 Informasi Umum")
col_a, col_b = st.columns(2)
with col_a:
    nama_guru = st.text_input("Nama Guru:", placeholder="Contoh: Ahmad Fauzi, S.Pd.I")
    nama_madrasah = st.text_input("Nama Madrasah:", placeholder="Contoh: MTsN 1 Kota")
with col_b:
    tahun_ajaran = st.text_input("Tahun Ajaran:", placeholder="Contoh: 2025/2026")
    alokasi_waktu = st.text_input("Alokasi Waktu:", placeholder="Contoh: 2 x 40 Menit")

st.markdown("---")
st.subheader("📖 Detail Materi")
jenjang = st.selectbox("Pilih Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")
topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Zakat Fitrah, Pembelahan Sel, dll")

generate_btn = st.button("✨ Generate Modul Ajar Sekarang")

if "hasil_modul" not in st.session_state:
    st.session_state.hasil_modul = ""

if generate_btn:
    if not mapel or not topik:
        st.warning("Mohon isi Mata Pelajaran dan Topik terlebih dahulu.")
    else:
        with st.spinner("⏳ Menyusun modul sesuai regulasi terbaru..."):
            try:
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                nama_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_list else model_list[0]
                model = genai.GenerativeModel(nama_model)
                
                # Prompt yang menggabungkan informasi umum dari user
                prompt = f"""
                Buatlah Modul Ajar Kurikulum Merdeka yang SEPENUHNYA PATUH pada Permendikdasmen No. 13 Tahun 2025 dan KMA No. 1503 Tahun 2025.

                IDENTITAS MODUL (Sertakan informasi ini di awal dalam bentuk TABEL):
                - Nama Guru: {nama_guru}
                - Instansi: {nama_madrasah}
                - Tahun Ajaran: {tahun_ajaran}
                - Mata Pelajaran: {mapel}
                - Jenjang/Fase: {jenjang}
                - Alokasi Waktu: {alokasi_waktu}
                - Topik: {topik}

                STRUKTUR ISI:
                1. TUJUAN PEMBELAJARAN (Kompetensi & Lingkup Materi).
                2. PROFIL PELAJAR: P3 (Pancasila) dan P2RA (Rahmatan Lil Alamin) sesuai KMA 1503/2025.
                3. LANGKAH PEMBELAJARAN (Berdiferensiasi: Pendahuluan, Inti, Penutup).
                4. ASESMEN (Awal, Formatif, Sumatif).
                5. MEDIA & SUMBER BELAJAR.

                INSTRUKSI FORMAT:
                - Gunakan Judul (Heading) yang jelas.
                - Gunakan Tabel untuk bagian identitas dan asesmen agar rapi saat dicopy ke Word.
                - JANGAN gunakan simbol bintang (**) berlebihan yang mengganggu mata. Gunakan format Markdown yang bersih.
                """
                
                response = model.generate_content(prompt)
                st.session_state.hasil_modul = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- AREA HASIL & PREVIEW ---
if st.session_state.hasil_modul:
    st.markdown("---")
    tab1, tab2 = st.tabs(["✨ Tampilan Rapi (SIAP COPAS)", "📝 Edit Teks"])
    
    with tab1:
        st.subheader("📄 Preview Modul Ajar")
        # Menampilkan teks yang sudah diformat tebal/tabel secara otomatis
        st.write(st.session_state.hasil_modul)
        st.divider()
        st.success("✅ **CARA PINDAH KE WORD:** Blok teks di atas, klik kanan Copy, lalu Paste di Word. Format akan otomatis rapi.")

    with tab2:
        st.session_state.hasil_modul = st.text_area("Editor:", value=st.session_state.hasil_modul, height=500)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(label="📥 Download .txt", data=st.session_state.hasil_modul, file_name=f"Modul_{mapel}.txt", mime="text/plain")
    with col2:
        if st.button("🗑️ Hapus & Buat Baru"):
            st.session_state.hasil_modul = ""
            st.rerun()

st.markdown("---")
st.caption("Aplikasi Modul Ajar Madrasah - Update Regulasi 2025/2026")
