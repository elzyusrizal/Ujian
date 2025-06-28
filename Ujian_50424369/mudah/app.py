

import flask
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

mock_tracking_data = {
    "JNE001": {"courier": "JNE", "status": "In Transit", "current_location": "Sorting Center Jakarta"},
    "TIKI002": {"courier": "TIKI", "status": "Out for Delivery", "current_location": "Bandung Hub"},
    "SICEPAT003": {"courier": "Sicepat", "status": "Delivered", "current_location": "Recipient's Address"},
    "JNT004": {"courier": "J&T", "status": "In Transit", "current_location": "Warehouse Surabaya"},
    "ANTERAJA005": {"courier": "Anteraja", "status": "At Pickup Point", "current_location": "Anteraja Point Grogol"},
}
valid_tracking_numbers = list(mock_tracking_data.keys())

@app.route('/track_package', methods=['GET'])
def track_package():
    tracking_num_param = request.args.get('tracking_number')
    delay = random.uniform(0.2, 0.8)
    time.sleep(delay)
    if tracking_num_param:
        tracking_num = tracking_num_param.upper()
        if tracking_num in mock_tracking_data:
            data = mock_tracking_data[tracking_num]
            data["tracking_number"] = tracking_num
            print(f"[SERVER] Sending status for {tracking_num}: {data} (after {delay:.2f}s delay)")
            return jsonify(data)
        else:
            error_msg = {"error": "tracking_not_found", "message": f"Tracking number '{tracking_num}' not found."}
            print(f"[SERVER] Tracking number {tracking_num} not found (after {delay:.2f}s delay)")
            return jsonify(error_msg), 404
    else:
        error_msg = {"error": "bad_request", "message": "Parameter 'tracking_number' is required."}
        return jsonify(error_msg), 400

if __name__ == '__main__':
    print("Simple Package Tracking API Server running on http://127.0.0.1:5000")
    print("Endpoint: GET /track_package?tracking_number=JNE001")
    app.run(debug=False, threaded=True, use_reloader=False)