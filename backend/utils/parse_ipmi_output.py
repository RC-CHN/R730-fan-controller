from influxdb_client import Point
def parse_ipmi_output(output):
    lines = output.strip().split('\n')
    data_points = []
    for line in lines[1:]:  # 跳过标题行
        parts = line.split('|')
        if len(parts) < 2:
            continue
        name = parts[0].strip()
        value = parts[1].strip()
        if value.lower() == 'na':
            continue
        try:
            value = float(value)
        except ValueError:
            continue
        unit = parts[2].strip()
        point = Point("ipmi_sensor").tag("sensor", name).field("value", value).tag("unit", unit)
        data_points.append(point)
    return data_points
