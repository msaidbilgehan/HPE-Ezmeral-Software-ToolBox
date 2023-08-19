import threading


 
class Task_Handler_Thread(threading.Thread):
      def __init__(self, task, parameters:list, *args, **kwargs):
         super(Task_Handler_Thread, self).__init__(*args, **kwargs)
         self.task = task
         self.parameters = parameters
         
         self.daemon = True
 
      def run(self):
         self.task(
            *self.parameters
         )
    
      def stop_Thread(self):
         self.join()
         return 0