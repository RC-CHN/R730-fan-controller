# api/endpoints/fan_speed.py
from flask import request, jsonify
from utils.ipmi_client import set_fan_speed

# 模式开关，假设在其他文件中已定义
from api.endpoints.mode import is_fixed_mode, fixed_speed

def api_fan_speed():
    global fixed_speed
    if request.method == 'GET':
        print("Received request: GET /api/fan_speed")
        # 获取当前风扇转速，只允许在固定模式下获取
        if not is_fixed_mode:
            print("Fan speed can only be retrieved in fixed mode.")
            return jsonify({'status': 'error', 'message': 'Fan speed can only be retrieved in fixed mode'}), 403
        
        # 返回当前的风扇速度
        return jsonify({'status': 'success', 'speed': fixed_speed})

    elif request.method == 'POST':
        data = request.get_json()
        print(f"Received request: POST /api/fan_speed with data: {data}")
        speed = data.get('speed')
        
        # 仅允许在固定模式下设置风扇速度
        if not is_fixed_mode:
            print("Fan speed adjustment is only allowed in fixed speed mode.")
            return jsonify({'status': 'error', 'message': 'Fan speed can only be set in fixed mode'}), 403
        
        # 验证 speed 值，并且设置新的风扇速度
        if isinstance(speed, int) and 0 <= speed <= 100:
            success = set_fan_speed(speed)
            if success:
                fixed_speed = speed
                print(f"Successfully set fixed fan speed to: {speed}")
                return jsonify({'status': 'success', 'speed': speed})
            else:
                print("Failed to set fan speed")
                return jsonify({'status': 'error', 'message': 'Failed to set fan speed'}), 500
        else:
            print("Invalid speed value received")
            return jsonify({'status': 'error', 'message': 'Invalid speed value'}), 400
