import subprocess
import os
import json

# 从配置文件读取配置信息
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# IPMI 配置
IPMI_HOST = config['ipmi']['host']
IPMI_USERNAME = config['ipmi']['username']
IPMI_PASSWORD = config['ipmi']['password']

def get_ipmi_sensor_data():
    print(f"Executing IPMI command to get sensor data from {IPMI_HOST}...")
    result = subprocess.check_output([
        'ipmitool', '-I', 'lanplus', '-H', IPMI_HOST, '-U', IPMI_USERNAME, '-P', IPMI_PASSWORD, 'sensor'
    ]).decode('utf-8')
    #print(f"IPMI command result: {result}")
    return result

def set_fan_speed(speed):
    if 0 <= speed <= 100:
        hex_speed = hex(speed)
        cmd = [
            'ipmitool', '-I', 'lanplus', '-H', IPMI_HOST, '-U', IPMI_USERNAME, '-P', IPMI_PASSWORD,
            'raw', '0x30', '0x30', '0x02', '0xff', hex_speed
        ]
        print(f"Setting fan speed to {speed}% using command: {cmd}")
        try:
            subprocess.call(cmd)
            print("Fan speed set successfully.")
            return True
        except Exception as e:
            print(f"Error setting fan speed: {e}")
            return False
    else:
        print(f"Invalid fan speed value: {speed}. Must be between 0 and 100.")
        return False

def set_manual_fan_mode():
    cmd = [
        'ipmitool', '-I', 'lanplus', '-H', IPMI_HOST, '-U', IPMI_USERNAME, '-P', IPMI_PASSWORD,
        'raw', '0x30', '0x30', '0x01', '0x00'
    ]
    print(f"Setting fan mode to manual using command: {cmd}")
    try:
        subprocess.call(cmd)
        print("Fan mode set to manual successfully.")
    except Exception as e:
        print(f"Error setting fan mode to manual: {e}")
