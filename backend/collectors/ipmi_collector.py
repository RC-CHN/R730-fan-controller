import time
from utils.ipmi_client import get_ipmi_sensor_data
from utils.influxdb_client import write_data_points
from utils.parse_ipmi_output import parse_ipmi_output

def start_ipmi_collector():
    time.sleep(5)
    while True:
        try:
            print("Collecting IPMI data...")
            result = get_ipmi_sensor_data()
            #print(f"IPMI data collected: {result}")
            data_points = parse_ipmi_output(result)
            #print(f"Parsed data points: {data_points}")
            write_data_points(data_points)
            print("Data points written to InfluxDB.")
            time.sleep(5)
        except Exception as e:
            print(f"Error collecting IPMI data: {e}")
            time.sleep(5)
