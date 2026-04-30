#!/usr/bin/env python3
import sys

current_factory = None
current_count = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    factory, count = line.split("\t")
    count = int(count)

    if current_factory == factory:
        current_count += count
    else:
        if current_factory is not None:
            print(f"{current_factory}\t{current_count}")

        current_factory = factory
        current_count = count

if current_factory is not None:
    print(f"{current_factory}\t{current_count}")
