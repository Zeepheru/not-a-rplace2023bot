import time

def get_time_passed(start_time):
    time_passed = time.time() - start_time
    h, remainder = divmod(time_passed, 3600)
    m, s = divmod(remainder, 60)
    ms = int((s % 1) * 1000)  # Getting milliseconds part

    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{ms:03d}"