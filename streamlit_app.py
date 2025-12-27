import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Modul Ajar Madrasah", page_icon="📚")

# --- KONFIGURASI API ---
try:
    # Mengambil API_KEY dari Secrets Streamlit
    KEY_NYA = st.secrets["API_KEY"]
    genai.configure(api_key=KEY_NYA)
except:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# --- TAMPILAN ---
st.title("📚 Penyusun Modul Ajar Madrasah")
st.write("Gunakan AI untuk menyusun Modul Ajar Kurikulum Merdeka.")

jenjang = st.selectbox("Pilih Jenjang:", ["MTs (Fase D)", "MA (Fase E)", "MA (Fase F)"])
mapel = st.text_input("Mata Pelajaran:")
topik = st.text_area("Topik Materi / Judul Bab:")

if st.button("✨ Generate Modul Ajar"):
    if not mapel or not topik:
        st.warning("Isi dulu Mapel dan Topiknya ya.")
    else:
        with st.spinner("Sedang mencari model AI yang tersedia..."):
            try:
                # LANGKAH ANTI-ERROR 404: Mencari model yang aktif di akun kamu
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Memilih model terbaik yang tersedia (Flash atau Pro)
                nama_model = ""
                if 'models/gemini-1.5-flash' in model_list:
                    nama_model = 'models/gemini-1.5-flash'
                elif 'models/gemini-1.5-pro' in model_list:
                    nama_model = 'models/gemini-1.5-pro'
                else:
                    nama_model = model_list[0] # Pakai apa saja yang tersedia

                model = genai.GenerativeModel(nama_model)
                
                prompt = f"""
                Buatkan Modul Ajar Kurikulum Merdeka untuk {jenjang}.
                Mata Pelajaran: {mapel}
                Topik: {topik}
                
                Struktur: Identitas, Profil Pelajar Pancasila & Rahmatan Lil Alamin, 
                Tujuan Pembelajaran, Langkah-langkah Kegiatan, dan Asesmen.
                Gunakan Bahasa Indonesia yang baik.
                """
                
                response = model.generate_content(prompt)
                
                st.success(f"Berhasil menggunakan {nama_model}")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Maaf, ada kendala teknis: {e}")

st.markdown("---")
st.caption("Dibuat untuk Guru Madrasah Indonesia")
    mapel = st.text_input("Mata Pelajaran:", placeholder="Contoh: Fikih, Biologi, Ekonomi")

topik = st.text_area("Topik Materi / Judul Bab:", placeholder="Contoh: Shalat Jamak dan Qashar, Sel, atau Permintaan dan Penawaran")

# --- PROSES GENERATE ---
if st.button("✨ Generate Modul Ajar"):
    if not mapel or not topik:
        st.warning("Silakan isi Mata Pelajaran dan Topik Materi terlebih dahulu.")
    else:
        with st.spinner("Sedang menyusun modul ajar yang lengkap..."):
            try:
                # Gunakan nama model tanpa prefix 'models/' atau coba versi pro jika flash bermasalah
                # Kita coba 'gemini-1.5-flash-latest' yang biasanya lebih stabil untuk API v1
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                prompt_lengkap = f"""
                Anda adalah pakar Kurikulum Merdeka Kemenag. 
                Buat Modul Ajar lengkap untuk {jenjang}, Mapel: {mapel}, Topik: {topik}.
                Sertakan Identitas, Profil Pelajar Pancasila & Rahmatan Lil Alamin, Tujuan, 
                Langkah Pembelajaran Aktif, dan Asesmen.
                """
                
                # Tambahkan sedikit konfigurasi pengamanan
                response = model.generate_content(prompt_lengkap)
                
                st.success("Berhasil! Modul ajar Anda telah siap.")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # Jika masih error 404, coba otomatis ganti ke model pro
                try:
                    model_alt = genai.GenerativeModel('gemini-1.5-pro')
                    response = model_alt.generate_content(prompt_lengkap)
                    st.markdown(response.text)
                except:
                    st.error(f"Terjadi kesalahan teknis: {e}")

                
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
