# api/endpoints/fan_curve.py
from flask import request, jsonify
from utils.fan_curve import fan_curve, fan_curve_lock

def api_fan_curve():
    global fan_curve
    if request.method == 'GET':
        print("Received request: GET /api/fan_curve")
        with fan_curve_lock:
            print(f"Returning fan curve: {fan_curve}")
            return jsonify(fan_curve)
    elif request.method == 'POST':
        new_curve = request.get_json()
        print(f"Received request: POST /api/fan_curve with data: {new_curve}")
        if isinstance(new_curve, list):
            with fan_curve_lock:
                fan_curve[:] = new_curve
            print(f"Updated fan curve: {fan_curve}")
            return jsonify({'status': 'success'})
        else:
            print("Invalid data format received for fan curve")
            return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400
