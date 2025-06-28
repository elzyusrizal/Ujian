import requests
import threading
import time
from datetime import datetime

BASE_API_URL = "http://127.0.0.1:5000/track_package"
TRACKING_NUMBERS_TO_CHECK = ["JNE001", "TIKI002", "INVALID123", "JNT004", "SICEPAT003"]
NUM_REQUESTS = len(TRACKING_NUMBERS_TO_CHECK)
CLIENT_LOG_FILE = "package_tracker_log.txt"

client_log_lock = threading.Lock()

with open(CLIENT_LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Package Tracker Log Started: {datetime.now()} ---\n")

# ==============================================================================
# SOAL 1: Implementasi Logging Thread-Safe
# ==============================================================================
def log_client_activity_safe(thread_name, message):
    """
    TUGAS ANDA (Soal 1):
    Lengkapi fungsi ini untuk mencatat 'message' dari 'thread_name' ke
    CLIENT_LOG_FILE secara thread-safe menggunakan 'client_log_lock'.

    Langkah-langkah:
    1. Dapatkan 'client_log_lock' (gunakan 'with' statement untuk kemudahan).
    2. Buat timestamp (contoh: datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")).
    3. Format pesan log (contoh: f"[{timestamp}] [{thread_name}] {message}\n").
    4. Tulis pesan log ke CLIENT_LOG_FILE (mode append 'a', encoding 'utf-8').
    5. (Opsional) Cetak pesan log ke konsol juga.
    """
    with client_log_lock:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        log_message = f"[{timestamp}] [{thread_name}] {message}\n"
        with open(CLIENT_LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_message)
        print(log_message.strip())


# ==============================================================================
# SOAL 2: Implementasi Fungsi Permintaan API
# ==============================================================================
def request_tracking_from_api(tracking_number, current_thread_name):
    """
    TUGAS ANDA (Soal 2):
    Lengkapi fungsi ini untuk mengirim permintaan GET ke API pelacakan paket
    dan mencatat hasilnya menggunakan fungsi 'log_client_activity_safe' yang
    telah Anda implementasikan di Soal 1.

    Langkah-langkah:
    1. Bentuk 'target_url' dengan menggunakan BASE_API_URL dan 'tracking_number' yang diberikan.
    2. Catat (menggunakan 'log_client_activity_safe') bahwa permintaan akan dikirim.
    3. Gunakan blok 'try-except' untuk menangani potensi error saat request.
       a. Di dalam 'try':
          i.  Kirim permintaan GET ke 'target_url' menggunakan 'requests.get()'. Sertakan timeout.
          ii. Periksa 'response.status_code':
              - Jika 200 (sukses):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan sukses. Contoh: f"Berhasil! Paket {data.get('tracking_number', tracking_number)} ({data.get('courier', 'N/A')}) status: {data.get('status', 'N/A')} di {data.get('current_location', 'N/A')}."
              - Jika 404 (nomor resi tidak ditemukan):
                  - Dapatkan JSON dari 'response.json()'.
                  - Catat pesan error. Contoh: f"Error: Nomor Resi {tracking_number} tidak ditemukan. Pesan: {data.get('message', 'Not found')}"
              - Untuk status code lain:
                  - Catat pesan error umum. Contoh: f"Menerima status error dari API: {response.status_code} - {response.text[:100]}"
       b. Di blok 'except requests.exceptions.Timeout':
          - Catat pesan timeout.
       c. Di blok 'except requests.exceptions.RequestException as e':
          - Catat pesan error permintaan umum.
       d. Di blok 'except Exception as e':
          - Catat pesan kesalahan tak terduga.
    4. Setelah blok try-except, catat bahwa tugas untuk nomor resi ini selesai.
    """
    target_url = f"{BASE_API_URL}?tracking_number={tracking_number}"
    log_client_activity_safe()
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            log_client_activity_safe(current_thread_name, f"Berhasil! Paket {data.get('tracking_number', tracking_number)} ({data.get('courier', 'N/A')}) status: {data.get('status', 'N/A')} di {data.get('current_location', 'N/A')}.")
            
        elif response.status_code == 400:
            data = response.json()
            log_client_activity_safe(current_thread_name, f"Error: Nomor Resi {tracking_number} tidak ditemukan. Pesan: {data.get('message', 'Not found')}")
            
        else:
            log_client_activity_safe(current_thread_name, f"Menerima status error dari API: {response.status_code} - {response.text[:100]}")
    
    except requests.exceptions.Timeout:
        log_client_activity_safe(current_thread_name, f"Permintaan Timeout.")
    except requests.exceptions.RequestException as e:
        log_client_activity_safe(current_thread_name, f"Permintaan Error. Error: {str(e)}")
    except Exception as e:
        log_client_activity_safe(current_thread_name, f"Kesalahan Tak Terduga.")
     
    log_client_activity_safe(current_thread_name, f"Tugas Selesai untuk nomor resi: {tracking_num}.")

def worker_thread_task(tracking_number, task_id):
    """Fungsi yang dijalankan oleh setiap worker thread."""
    thread_name = f"Worker-{task_id}"
    log_client_activity_safe(thread_name, f"Memulai pelacakan untuk No. Resi: {tracking_number}")
    request_tracking_from_api(tracking_number, thread_name)
    log_client_activity_safe(thread_name, f"Selesai pelacakan untuk No. Resi: {tracking_number}")

if __name__ == "__main__":
    log_client_activity_safe("MainClient", f"Memulai {NUM_REQUESTS} pelacakan paket secara concurrent.")
    
    threads = []
    start_time = time.time()

    for i, tracking_num in enumerate(TRACKING_NUMBERS_TO_CHECK):
        thread = threading.Thread(target=worker_thread_task, args=(tracking_num, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    log_client_activity_safe("MainClient", f"Semua pelacakan paket selesai dalam {total_time:.2f} detik.")
    print(f"\nLog aktivitas klien disimpan di: {CLIENT_LOG_FILE}")
    print(f"Total waktu eksekusi: {total_time:.2f} detik.")