import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚")

# --- KONFIGURASI API ---
try:
    # Mengambil API_KEY dari Secrets Streamlit
    KEY_NYA = st.secrets["API_KEY"]
    genai.configure(api_key=KEY_NYA)
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# --- TAMPILAN ---
st.title("📚 Penyusun Modul Ajar Madrasah")
st.write("Gunakan AI untuk menyusun Modul Ajar Kurikulum Merdeka.")

jenjang = st.selectbox("Pilih Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")
topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Zakat Fitrah, Sel, dll")

if st.button("✨ Generate Modul Ajar"):
    if not mapel or not topik:
        st.warning("Isi dulu Mapel dan Topiknya ya.")
    else:
        with st.spinner("Sedang menyusun modul ajar..."):
            try:
                # Mencari model yang aktif di akun Anda secara otomatis
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Memilih model terbaik yang tersedia
                nama_model = ""
                if 'models/gemini-1.5-flash' in model_list:
                    nama_model = 'models/gemini-1.5-flash'
                elif 'models/gemini-1.5-pro' in model_list:
                    nama_model = 'models/gemini-1.5-pro'
                elif 'models/gemini-pro' in model_list:
                    nama_model = 'models/gemini-pro'
                else:
                    nama_model = model_list[0] if model_list else ""

                if not nama_model:
                    st.error("Tidak ada model AI yang ditemukan pada API Key ini.")
                else:
                    model = genai.GenerativeModel(nama_model)
                    
                    prompt = f"""
                    Buatkan Modul Ajar Kurikulum Merdeka untuk {jenjang}.
                    Mata Pelajaran: {mapel}
                    Topik: {topik}
                    
                    Struktur: Identitas, Profil Pelajar Pancasila & Rahmatan Lil Alamin, 
                    Tujuan Pembelajaran, Langkah-langkah Kegiatan, dan Asesmen.
                    Gunakan Bahasa Indonesia yang baik dan formal.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.success(f"Berhasil menggunakan {nama_model}")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.info("💡 Tips: Anda bisa blok teks di atas, lalu Copy ke MS Word.")
                
            except Exception as e:
                st.error(f"Maaf, ada kendala teknis: {e}")

st.markdown("---")
st.caption("Dibuat untuk Guru Madrasah Indonesia")
