# logger_util.py
from collections import deque

log_buffer = deque(maxlen=1000)

def add_log(message):
    print(message)  # 可选：也输出到终端
    log_buffer.append(message)

def get_logs():
    return list(log_buffer)
