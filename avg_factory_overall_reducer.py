#!/usr/bin/env python3
import sys

current_key = None
total_value = 0
total_count = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    key, value_count = line.split("\t")
    value, count = value_count.split(",")

    value = float(value)
    count = int(count)

    if current_key == key:
        total_value += value
        total_count += count
    else:
        if current_key is not None:
            average = total_value / total_count
            print(f"{current_key}\t{average:.2f}")

        current_key = key
        total_value = value
        total_count = count

if current_key is not None:
    average = total_value / total_count
    print(f"{current_key}\t{average:.2f}")
