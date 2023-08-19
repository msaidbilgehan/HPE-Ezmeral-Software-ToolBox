import threading


 
class Task_Handler_Thread(threading.Thread):
      def __init__(self, task, parameters:dict, *args, **kwargs):
         super(Task_Handler_Thread, self).__init__(*args, **kwargs)
         self.task = task
         self.parameters = parameters
         
         self.daemon = True
 
      def set_Parameters(self, parameters:dict):
         self.parameters = parameters
 
      def run(self):
         self.task(
            **self.parameters
         )
    
      def stop_Thread(self):
         self.join()
         return 0