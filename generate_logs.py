import random
from datetime import datetime, timedelta

sensor_types = ["temperature", "vibration", "pressure", "humidity"]
factories = ["Factory-A", "Factory-B", "Factory-C", "Factory-D"]
machine_lines = ["Line-1", "Line-2", "Line-3", "Line-4"]

start_time = datetime.now()
output_file = "../data/sensor_logs.csv"

with open(output_file, "w") as file:
    file.write("timestamp,sensor_id,sensor_type,value,factory,line,status\n")

    for i in range(50000):
        timestamp = start_time + timedelta(seconds=i)
        sensor_id = f"sensor_{random.randint(1, 1000):04d}"
        sensor_type = random.choice(sensor_types)
        factory = random.choice(factories)
        line = random.choice(machine_lines)

        if sensor_type == "temperature":
            value = round(random.uniform(20, 130), 2)
        elif sensor_type == "vibration":
            value = round(random.uniform(0, 80), 2)
        elif sensor_type == "pressure":
            value = round(random.uniform(50, 180), 2)
        else:
            value = round(random.uniform(20, 95), 2)

        if sensor_type == "temperature" and value > 100:
            status = "ERROR"
        elif sensor_type == "vibration" and value > 60:
            status = "ERROR"
        elif sensor_type == "pressure" and value > 150:
            status = "ERROR"
        elif sensor_type == "humidity" and value > 80:
            status = "ERROR"
        elif value > 70:
            status = "WARN"
        else:
            status = "OK"

        file.write(f"{timestamp},{sensor_id},{sensor_type},{value},{factory},{line},{status}\n")

print("sensor_logs.csv generated successfully with 50,000 records.")
