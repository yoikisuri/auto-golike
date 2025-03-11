import time


def countdown(delay):
    end_time = time.time() + delay
    remaining = round(end_time - time.time(), 3)
    positions = ["X    ", " X   ", "  X  ", "   X ", "    X"]
    pos = 0
    while remaining > 0:
        print(f"[YOIKISURI][{remaining:.3f}][{positions[pos]}]", end=" \r", flush=True)
        remaining = max(0, round(end_time - time.time(), 3))
        time.sleep(0.01)
        pos = (pos + 1) % len(positions)
