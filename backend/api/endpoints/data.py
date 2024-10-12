# api/endpoints/data.py
from flask import jsonify
from utils.influxdb_client import get_latest_sensor_data

def api_get_data():
    print("Received request: GET /api/data")
    data = get_latest_sensor_data()
    print(f"Returning sensor data: {data}")
    return jsonify(data)
