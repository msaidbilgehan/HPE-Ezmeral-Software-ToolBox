import time


def read_log_file(path, wait_thread=None):
    with open(path, 'r') as file:
        while True:
            line = file.readline().strip()
            if line:
                # print(line)
                yield f"data: {line}\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)
            
            time.sleep(1)  # Wait for new content
            
            if wait_thread is not None:
                if not wait_thread.is_alive():
                    break