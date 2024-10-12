import os
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# 从配置文件读取配置信息
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '..', 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

# InfluxDB 配置
INFLUXDB_URL = config['influxdb']['url']
INFLUXDB_USERNAME = config['influxdb']['username']
INFLUXDB_PASSWORD = config['influxdb']['password']
INFLUXDB_ORG = config['influxdb']['org']
INFLUXDB_BUCKET = config['influxdb']['bucket']

print(f"Connecting to InfluxDB at {INFLUXDB_URL} with user {INFLUXDB_USERNAME}...")
influxdb_client = InfluxDBClient(
    url=INFLUXDB_URL,
    username=INFLUXDB_USERNAME,
    password=INFLUXDB_PASSWORD,
    org=INFLUXDB_ORG
)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
query_api = influxdb_client.query_api()
print("Connected to InfluxDB.")

def write_data_points(data_points):
    #print(f"Writing data points to InfluxDB: {data_points}")
    for point in data_points:
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print("Data points written successfully.")

def get_current_temperature():
    print("Querying current temperature from InfluxDB...")
    query = f'''from(bucket:"{INFLUXDB_BUCKET}")
                |> range(start: -5m)
                |> filter(fn: (r) => r._measurement == "ipmi_sensor" and r.sensor == "Temp")
                |> last()'''
    result = query_api.query(org=INFLUXDB_ORG, query=query)
    
    temps = []
    for table in result:
        for record in table.records:
            temp = record.get_value()
            temps.append(temp)
            print(f"Found temperature value: {temp}")
    
    if temps:
        # 计算两个温度的平均值
        average_temp = sum(temps) / len(temps)
        print(f"Average temperature: {average_temp}")
        return average_temp
    else:
        print("No temperature data found.")
        return None


def get_latest_sensor_data():
    print("Querying latest sensor data from InfluxDB...")
    query = f'''from(bucket:"{INFLUXDB_BUCKET}")
                |> range(start: -5m)
                |> filter(fn: (r) => r._measurement == "ipmi_sensor")
                |> last()'''
    result = query_api.query(org=INFLUXDB_ORG, query=query)
    data = {}
    for table in result:
        for record in table.records:
            sensor_name = record['sensor']
            value = record.get_value()
            data[sensor_name] = value
    print(f"Latest sensor data: {data}")
    return data
