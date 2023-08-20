

 
import os
import threading
import time



class File_Content_Streamer_Thread(threading.Thread):
    def __init__(self, path, wait_thread=None, is_yield=False, content_control=True, *args, **kwargs):
        super(File_Content_Streamer_Thread, self).__init__(*args, **kwargs)
        
        self.wait_thread = wait_thread
        self.path = path
        self.is_yield = is_yield
        self.content_control = content_control
        
        self.__string_stream = ""
        
        self._flag_stop = False
        self.is_running = False
        self.daemon = True


    def run(self) -> None:
        self.is_running = True
        self.read_file_continues(
            wait_thread=self.wait_thread,
            is_yield=self.is_yield,
            store_in_buffer=True,
            is_print=False,
            sleep_time=1,
            content_control=self.content_control
        )
        self.is_running = False
    

    def read_file_continues(self, wait_thread=None, is_yield=False, store_in_buffer=True, is_print=False, sleep_time=1., new_sleep_time=1., content_control=True):
        time.sleep(1)
        
        if content_control:
            if os.path.exists(self.path):
                if os.stat(self.path).st_size != 0:
                    yield from self.read_action(
                        wait_thread=wait_thread,
                        is_yield=is_yield,
                        store_in_buffer=store_in_buffer,
                        is_print=is_print,
                        sleep_time=sleep_time,
                        new_sleep_time=new_sleep_time
                    )
                else:
                    yield f"data: No Logs Found\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)
            else:
                yield f"data: No Logs File Found\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)
        else:
            yield from self.read_action(
                wait_thread=wait_thread,
                is_yield=is_yield,
                store_in_buffer=store_in_buffer,
                is_print=is_print,
                sleep_time=sleep_time,
                new_sleep_time=new_sleep_time
            )

    def read_action(self, wait_thread=None, is_yield=False, store_in_buffer=True, is_print=False, sleep_time=1., new_sleep_time=1.):
        self._flag_stop = False
                
        current_sleep_time = sleep_time
        with open(self.path, 'r') as file:
            while not self._flag_stop:
                raw_line = file.readline()
                if raw_line == '':
                    current_sleep_time = new_sleep_time
                    
                line = raw_line.strip()
                if line:
                    if is_print:
                        print(line)
                    if store_in_buffer:
                        self.__string_stream += f"{line}\n"
                    if is_yield:
                        yield f"data: {line}\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)
                
                if current_sleep_time > 0:
                    time.sleep(current_sleep_time)  # Wait for new content
                
                if wait_thread is not None:
                    if not wait_thread.is_alive():
                        break


    def read_Buffer(self, convert_for_HTML=False) -> str:
        if convert_for_HTML:
            return self.__string_stream.replace("\n", "<br>")
        else:
            return self.__string_stream
    

    def clear_Buffer(self) -> None:
        self.__string_stream = ""
        

    def clear_File_Content(self) -> None:
        open(self.path, 'w').close()
    

    def delete_File(self) -> int:
        if os.path.exists(self.path):
            os.remove(self.path)
            return 0
        return -1
    

    def stop_Thread(self) -> str:
        self._flag_stop = True
        self.join()
        return self.__string_stream