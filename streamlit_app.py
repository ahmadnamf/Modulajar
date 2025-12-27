import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AI Pembuat Modul Ajar Madrasah",
    page_icon="📚",
    layout="centered"
)

# --- KONFIGURASI API KEY ---
# Kode ini akan mengambil API Key dari menu "Secrets" di Streamlit agar aman
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key tidak ditemukan! Pastikan Anda sudah memasukkannya di menu Settings > Secrets di Streamlit.")
    st.stop()

# --- TAMPILAN ANTARMUKA ---
st.title("📚 Penyusun Modul Ajar Madrasah")
st.write("Alat bantu AI untuk guru MTs & MA menyusun Modul Ajar Kurikulum Merdeka.")

with st.expander("ℹ️ Cara Penggunaan"):
    st.write("""
    1. Pilih Jenjang (MTs atau MA).
    2. Masukkan Mata Pelajaran.
    3. Masukkan Topik atau Bab yang ingin dibuatkan modunyal.
    4. Klik 'Generate Modul Ajar' dan tunggu AI bekerja.
    """)

# --- INPUT FORM ---
col1, col2 = st.columns(2)
with col1:
    jenjang = st.selectbox("Pilih Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
with col2:
    mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")

topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Shalat Jamak dan Qashar, Sel, atau Permintaan dan Penawaran")

# --- PROSES GENERATE ---
if st.button("✨ Generate Modul Ajar"):
    if not mapel or not topik:
        st.warning("Silakan isi Mata Pelajaran dan Topik Materi terlebih dahulu.")
    else:
        with st.spinner("Sedang menyusun modul ajar yang lengkap..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Instruksi sistem yang sangat mendalam
                prompt_lengkap = f"""
                Bertindaklah sebagai Konsultan Kurikulum Merdeka di Kemenag RI.
                Buatkan Modul Ajar yang lengkap dan profesional untuk:
                Jenjang: {jenjang}
                Mata Pelajaran: {mapel}
                Topik: {topik}

                Struktur Modul Ajar harus mengikuti komponen berikut:
                1. IDENTITAS MODUL: Nama sekolah, Tahun, Jenjang, Alokasi Waktu.
                2. KOMPETENSI AWAL: Kemampuan yang diperlukan siswa.
                3. PROFIL PELAJAR PANCASILA & RAHMATAN LIL ALAMIN: Sebutkan minimal 3 nilai (Contoh: Berkeadaban/Ta’addub, Keteladanan/Qudwah, Syura, dll).
                4. SARANA & PRASARANA: Daftar alat dan bahan.
                5. TARGET PESERTA DIDIK & MODEL PEMBELAJARAN: Gunakan model aktif seperti Discovery Learning atau PBL.
                6. KOMPONEN INTI: Tujuan Pembelajaran, Pemahaman Bermakna, Pertanyaan Pemantik.
                7. KEGIATAN PEMBELAJARAN: Langkah-langkah Pendahuluan, Inti, dan Penutup secara mendetail.
                8. ASESMEN: Diagnostik, Formatif, dan Sumatif.
                9. PENGAYAAN & REMEDIAL.
                
                Gunakan bahasa Indonesia yang formal, edukatif, dan mudah dipahami oleh guru.
                """
                
                response = model.generate_content(prompt_lengkap)
                
                # Menampilkan Hasil
                st.success("Berhasil! Modul ajar Anda telah siap.")
                st.markdown("---")
                st.markdown(response.text)
                
                # Fitur Copy sederhana
                st.info("💡 Anda bisa menyalin teks di atas dan memindahkannya ke Microsoft Word.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Dibuat untuk membantu Guru Madrasah Indonesia | Berbasis Google Gemini AI")
