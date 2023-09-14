from queue import Queue
import time

from Flask_App.Classes.Task_Handler import Task_Handler_Class



class Notification_Status:
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"



class Notification_Handler_Thread(Task_Handler_Class):
    def __init__(self, wait_thread=None, *args, **kwargs):
        super(Notification_Handler_Thread, self).__init__(*args, **kwargs)
        
        self.wait_thread = wait_thread
        
        self.__notification_buffer: Queue[dict[str, str]] = Queue()
        self.__notification_structure: dict[str, str] = {
            "message": "",
            "status": Notification_Status.INFO,
        }


    def set_Parameters(self) -> int:
        return 0
   

    def task(self):
        yield from self.streamer(
            wait_thread=self.wait_thread,
            sleep_time=1,
        )
        

    def streamer(self, wait_thread=None, sleep_time=1.):
      self.is_running = False
      self.is_finished = False
      
      while not self.is_Thread_Stopped():
         while not self.is_Task_Stopped():
            
            self.is_running = True
            self.is_finished = False

            # Thread Sleep for sync
            if sleep_time > 0:
                time.sleep(sleep_time)  # Wait for new content
            
            # Check if wait_thread is alive
            if wait_thread is not None:
                if not wait_thread.is_alive():
                    break
            
            # Check if buffer is empty
            if self.__notification_buffer.empty():
                continue
            
            # Get content from buffer and stream it
            yield f"data: {self.queue_get()}\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)

        
    def queue_add(self, message: str="", status: str=Notification_Status.INFO):
        temp_nof = self.__notification_structure.copy()
        
        temp_nof["message"] = message
        
        if status not in [Notification_Status.INFO, Notification_Status.INFO, Notification_Status.WARNING, Notification_Status.ERROR]:
            temp_nof["status"] = Notification_Status.UNKNOWN
            
        temp_nof["status"] = status
        
        self.__notification_buffer.put(temp_nof)
        
        
    def queue_clear(self):
        self.__notification_buffer.queue.clear()
        
        
    def queue_size(self):
        return self.__notification_buffer.qsize()
    
    
    def queue_get(self):
        return self.__notification_buffer.get()