import threading
from flask import Flask
from api.routes import init_api
from collectors.ipmi_collector import start_ipmi_collector
from controllers.fan_controller import start_fan_controller
from utils.ipmi_client import set_manual_fan_mode

app = Flask(__name__)

# 初始化 Flask 路由
init_api(app)

if __name__ == '__main__':
    print("Starting IPMI data collector thread...")
    threading.Thread(target=start_ipmi_collector, daemon=True).start()
    
    print("Starting fan speed adjustment thread...")
    threading.Thread(target=start_fan_controller, daemon=True).start()
    
    print("Setting fan mode to manual...")
    set_manual_fan_mode()
    
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
