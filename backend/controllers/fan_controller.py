import time
import copy
from utils.fan_curve import fan_curve, fan_curve_lock
from utils.influxdb_client import get_current_temperature
from utils.ipmi_client import set_fan_speed
from utils.calculate_fan_speed import calculate_fan_speed

def start_fan_controller():
    time.sleep(5)
    while True:
        try:
            # 拷贝风扇曲线，减少锁的持有时间
            with fan_curve_lock:
                fan_curve_copy = copy.deepcopy(fan_curve)
            
            print("Adjusting fan speed...")
            if not fan_curve_copy:
                print("Fan curve is empty. Skipping adjustment.")
                time.sleep(5)
                continue

            current_temp = get_current_temperature()
            print(f"Current temperature: {current_temp}")
            if current_temp is None:
                print("No temperature data available. Skipping adjustment.")
                time.sleep(5)
                continue

            print("Current fan curve: " + str(fan_curve_copy))
            target_speed = calculate_fan_speed(current_temp, fan_curve_copy)
            print(f"Calculated target fan speed: {target_speed}")

            # 如果计算得到目标风扇速度，则设置速度
            if target_speed is not None:
                set_fan_speed(target_speed)
                print(f"Fan speed set to: {target_speed}")

            # 每次调整后等待 5 秒
            time.sleep(5)

        except Exception as e:
            print(f"Error adjusting fan speed: {e}")
            time.sleep(5)
