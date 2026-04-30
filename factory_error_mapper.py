#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith("timestamp"):
        continue

    parts = line.split(",")

    if len(parts) == 7:
        factory = parts[4]
        status = parts[6]

        if status == "ERROR":
            print(f"{factory}\t1")
