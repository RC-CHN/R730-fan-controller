# api/endpoints/mode.py
from flask import request, jsonify

# 模式开关，默认为动态调速模式
is_fixed_mode = False
fixed_speed = None
default_speed = 20

def api_mode():
    global is_fixed_mode
    if request.method == 'GET':
        print(f"Received request: GET /api/mode, current mode: {'fixed' if is_fixed_mode else 'dynamic'}")
        return jsonify({'mode': 'fixed' if is_fixed_mode else 'dynamic'})
    elif request.method == 'POST':
        data = request.get_json()
        new_mode = data.get('mode')
        if new_mode == 'fixed':
            is_fixed_mode = True
            fixed_speed = default_speed
            print("Switched to fixed speed mode.Default speed: "+str(fixed_speed))
            return jsonify({'status': 'success', 'mode': 'fixed'})
        elif new_mode == 'dynamic':
            is_fixed_mode = False
            print("Switched to dynamic speed mode.")
            return jsonify({'status': 'success', 'mode': 'dynamic'})
        else:
            print("Invalid mode received.")
            return jsonify({'status': 'error', 'message': 'Invalid mode'}), 400
