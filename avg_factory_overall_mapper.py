#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith("timestamp"):
        continue

    parts = line.split(",")

    if len(parts) == 7:
        sensor_type = parts[2]
        value = parts[3]
        factory = parts[4]

        try:
            value = float(value)

            # Average per factory and sensor type
            print(f"{factory}_{sensor_type}\t{value},1")

            # Overall average per sensor type
            print(f"OVERALL_{sensor_type}\t{value},1")

        except ValueError:
            continue
