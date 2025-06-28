

import requests
import threading
import time

# --- Konfigurasi Klien ---
BASE_API_URL = "http://127.0.0.1:5000"

# Data untuk diuji oleh klien: Daftar NIM yang akan diverifikasi
NIM_UNTUK_DIVERIFIKASI = ["2502012345", "2502034567", "9999999999", "2502045678"] # Satu NIM tidak ada

# ==============================================================================
# SOAL: Implementasi Fungsi untuk Verifikasi Status Mahasiswa via API
# ==============================================================================
def client_verifikasi_mahasiswa_via_api(nim, thread_name):
    """
    TUGAS ANDA:
    Lengkapi fungsi ini untuk mengambil informasi status akademik mahasiswa dari API
    dan mencetak hasilnya ke konsol.

    Langkah-langkah:
    1. Bentuk URL target: f"{BASE_API_URL}/mahasiswa/{nim}/status"
    2. Cetak pesan ke konsol bahwa thread ini ('thread_name') memulai verifikasi untuk 'nim'.
       Contoh: print(f"[{thread_name}] Memverifikasi NIM: {nim}")
    3. Gunakan blok 'try-except' untuk menangani potensi error saat melakukan permintaan HTTP.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke URL target menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan data JSON dari 'response.json()'.
                  - Cetak nama, status, dan IPK mahasiswa ke konsol.
                    Contoh: print(f"[{thread_name}] Mahasiswa {data.get('nama')} ({nim}): Status {data.get('status')}, IPK {data.get('ipk')}")
              - Jika 404 (NIM tidak ditemukan):
                  - Cetak pesan bahwa NIM tidak terdaftar.
                    Contoh: print(f"[{thread_name}] Mahasiswa dengan NIM {nim} tidak terdaftar.")
              - Untuk status code lain:
                  - Cetak pesan error umum ke konsol.
       b. Di blok 'except requests.exceptions.Timeout':
          - Cetak pesan bahwa permintaan timeout ke konsol.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Cetak pesan error permintaan umum ke konsol.
    4. Setelah blok try-except, cetak pesan ke konsol bahwa thread ini ('thread_name') selesai memproses 'nim'.
    """
    target_url = f"{BASE_API_URL}/mahasiswa/{nim}/status"
    print(f"[{thread_name}] Memverifikasi NIM: {nim}")
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[{thread_name}] Mahasiswa {data.get('nama')} ({nim}): Status {data.get('status')}, IPK {data.get('ipk')}")
        elif response.status_code == 400:
            print(f"[{thread_name}] Mahasiswa dengan NIM {nim} tidak terdaftar.")
        else:
            print(f"[{thread_name}] Error API untuk {nim}: Status {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[{thread_name}] Permintaan timeout untuk nim {nim}.")
    except requests.exceptions.RequestException as e:
        print(f"[{thread_name}] Permintaan gagal untuk nim {nim}. Error: {str(e)}")
    print(f"[{thread_name}] Selesai memproses nim: {nim}")

# --- Bagian Utama Skrip (Tidak Perlu Diubah Peserta) ---
if __name__ == "__main__":
    print(f"Memulai Klien Verifikasi untuk {len(NIM_UNTUK_DIVERIFIKASI)} Mahasiswa Secara Concurrent.")
    
    threads = []
    start_time = time.time()

    for i, nim_cek in enumerate(NIM_UNTUK_DIVERIFIKASI):
        thread_name_for_task = f"Verifikator-{i+1}" 
        thread = threading.Thread(target=client_verifikasi_mahasiswa_via_api, args=(nim_cek, thread_name_for_task))
        threads.append(thread)
        thread.start()

    for thread_instance in threads:
        thread_instance.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSemua verifikasi mahasiswa telah selesai diproses dalam {total_time:.2f} detik.")