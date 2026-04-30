#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith("timestamp"):
        continue

    parts = line.split(",")

    if len(parts) == 7:
        status = parts[6]
        print(f"{status}\t1")
