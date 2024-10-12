def calculate_fan_speed(temp, fan_curve):
    # 确保风扇曲线按温度升序排序
    sorted_curve = sorted(fan_curve, key=lambda x: x['temp'])
    for point in sorted_curve:
        if temp <= point['temp']:
            return point['speed']
    # 如果温度超过所有节点，返回最大转速
    return sorted_curve[-1]['speed']
