import math
import random
import os
import sys
import json
from datetime import datetime, timedelta
from statistics import mean, median, mode, stdev


def main():
    # Math module
    print("=== Math Module ===")
    print(f"Pi: {math.pi:.6f}")
    print(f"E: {math.e:.6f}")
    print(f"sqrt(16): {math.sqrt(16)}")
    print(f"sin(pi/2): {math.sin(math.pi / 2)}")
    print(f"floor(3.7): {math.floor(3.7)}")
    print(f"ceil(3.2): {math.ceil(3.2)}")

    # Random module
    print("\n=== Random Module ===")
    print(f"Random int [1,10]: {random.randint(1, 10)}")
    print(f"Random float [0,1): {random.random():.4f}")
    items = ["apple", "banana", "cherry", "date"]
    print(f"Random choice: {random.choice(items)}")
    random.shuffle(items)
    print(f"Shuffled list: {items}")
    print(f"Sample of 2: {random.sample(items, 2)}")

    # OS module
    print(f"\n=== OS Module ===")
    print(f"Current dir: {os.getcwd()}")
    print(f"User: {os.getenv('USER', 'unknown')}")
    print(f"OS name: {os.name}")
    print(f"CPU count: {os.cpu_count()}")

    # Datetime module
    print(f"\n=== Datetime Module ===")
    now = datetime.now()
    print(f"Now: {now}")
    print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    tomorrow = now + timedelta(days=1)
    print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")

    # Statistics module
    print(f"\n=== Statistics Module ===")
    data = [2, 3, 3, 4, 5, 5, 5, 6, 7]
    print(f"Data: {data}")
    print(f"Mean: {mean(data):.2f}")
    print(f"Median: {median(data)}")
    print(f"Mode: {mode(data)}")
    print(f"Std Dev: {stdev(data):.2f}")


if __name__ == "__main__":
    main()
