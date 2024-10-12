import threading

# 初始风扇曲线
fan_curve = [
    {"temp": 30, "speed": 5},
    {"temp": 40, "speed": 10},
    {"temp": 45, "speed": 15},
    {"temp": 50, "speed": 25},
    {"temp": 55, "speed": 30},
    {"temp": 60, "speed": 35},
    {"temp": 65, "speed": 40},
    {"temp": 70, "speed": 50},
    {"temp": 80, "speed": 80}
]

fan_curve_lock = threading.Lock()
