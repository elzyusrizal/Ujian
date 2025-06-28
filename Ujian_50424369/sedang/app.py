

import flask
from flask import Flask, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# Database simulasi data akademik mahasiswa
mahasiswa_db = {
    "2502012345": {"nama": "Budi Darmawan", "prodi": "Teknik Informatika", "status": "Aktif", "ipk": 3.85},
    "2502023456": {"nama": "Cindy Aulia", "prodi": "Sistem Informasi", "status": "Cuti", "ipk": 3.21},
    "2502034567": {"nama": "Eko Prasetyo", "prodi": "Teknik Informatika", "status": "Aktif", "ipk": 3.92},
    "2502045678": {"nama": "Fitriani", "prodi": "Desain Komunikasi Visual", "status": "Lulus", "ipk": 3.77},
}
db_lock = threading.Lock()

def log_server_activity(message):
    """Fungsi sederhana untuk logging di sisi server (ke konsol)."""
    print(f"[SERVER-AKADEMIK] {time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

@app.route('/mahasiswa/<nim>/status', methods=['GET'])
def get_status_mahasiswa(nim):
    """Endpoint untuk mendapatkan status akademik mahasiswa berdasarkan NIM."""
    log_server_activity(f"Permintaan status untuk NIM: {nim}")
    
    time.sleep(random.uniform(0.2, 0.6)) 
    
    with db_lock:
        mahasiswa = mahasiswa_db.get(nim)
    
    if mahasiswa:
        response_data = mahasiswa.copy()
        response_data["nim"] = nim
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "NIM tidak terdaftar"}), 404

if __name__ == '__main__':
    log_server_activity("API Status Akademik Mahasiswa dimulai.")
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)