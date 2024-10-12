# api/routes.py
from flask import Flask
from api.endpoints.data import api_get_data
from api.endpoints.fan_curve import api_fan_curve
from api.endpoints.fan_speed import api_fan_speed
from api.endpoints.mode import api_mode

def init_api(app: Flask):
    app.add_url_rule('/api/data', view_func=api_get_data, methods=['GET'])
    app.add_url_rule('/api/fan_curve', view_func=api_fan_curve, methods=['GET', 'POST'])
    app.add_url_rule('/api/fan_speed', view_func=api_fan_speed, methods=['GET','POST'])
    app.add_url_rule('/api/mode', view_func=api_mode, methods=['GET', 'POST'])
