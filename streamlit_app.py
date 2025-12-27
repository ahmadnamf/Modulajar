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
st.title("📚 Penyusun Modul Ajar Madrasah")
st.write("Gunakan AI untuk menyusun Modul Ajar Kurikulum Merdeka secara instan.")

jenjang = st.selectbox("Pilih Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")
topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Zakat Fitrah, Sel, dll")

if st.button("✨ Generate Modul Ajar"):
    if not mapel or not topik:
        st.warning("Isi dulu Mapel dan Topiknya ya.")
    else:
        with st.spinner("Sedang menyusun modul ajar..."):
            try:
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                nama_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_list else model_list[0]

                model = genai.GenerativeModel(nama_model)
                
                prompt = f"Buatkan Modul Ajar Kurikulum Merdeka untuk {jenjang}. Mapel: {mapel}. Topik: {topik}. Lengkap dengan Identitas, Profil Pelajar Pancasila & Rahmatan Lil Alamin, Tujuan, Langkah Kegiatan, dan Asesmen."
                
                response = model.generate_content(prompt)
                hasil_teks = response.text
                
                st.success("Berhasil menyusun modul!")
                st.markdown("---")

                # --- TOMBOL-TOMBOL DI ATAS HASIL ---
                col1, col2 = st.columns(2)
                
                with col1:
                    # Tombol Copy (menggunakan st.code karena paling stabil untuk copy)
                    st.write("📋 **Salin Teks di Bawah:**")
                
                with col2:
                    # Tombol Download sebagai file .doc / .txt agar bisa dibuka di Word/PDF
                    st.download_button(
                        label="📥 Simpan sebagai File (Word/PDF)",
                        data=hasil_teks,
                        file_name=f"Modul_Ajar_{mapel}_{topik}.txt",
                        mime="text/plain",
                    )
                
                # Menampilkan Hasil dalam kotak yang bisa di-copy
                st.code(hasil_teks, language="markdown")
                
                st.info("💡 **Tips:** Untuk membuat PDF, klik tombol Download di atas, buka filenya, lalu pilih 'Save as PDF' atau 'Print' dari perangkat Anda.")
                
            except Exception as e:
                st.error(f"Maaf, ada kendala teknis: {e}")

st.markdown("---")
st.caption("Dibuat untuk Guru Madrasah Indonesia")
