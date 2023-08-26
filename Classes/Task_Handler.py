
from abc import ABC, abstractmethod
import logging
from logging.handlers import RotatingFileHandler
import sys
import threading
import time

from Libraries.tools import list_dir



class Task_Handler_Class(ABC, threading.Thread):
   def __init__(self, logger=None, logger_level_stdo: int = logging.DEBUG, logger_level_file: int = logging.DEBUG, logger_file_path: str ="", mode="a", maxBytes=5*1024*1024, backupCount=2, *args, **kwargs):
      super(Task_Handler_Class, self).__init__(*args, **kwargs)

      self.logger_file_path = logger_file_path

      if logger is None:
         self.create_Logger(
            level_stdo=logger_level_stdo,
            level_file=logger_level_file,
            mode=mode, 
            maxBytes=maxBytes,
            backupCount=backupCount
         )
      else:
         self.logger = logger
      
      self.__parameters_template = {}
      self.parameters = self.__parameters_template.copy()

      # Flags
      self._flag_thread_stop = False
      self._flag_task_stop = True

      # Information
      self.is_running = False
      self.is_finished = False

      # Configuration
      self.daemon = True
            
            
   def create_Logger(self, level_stdo: int = logging.DEBUG, level_file: int = logging.DEBUG, mode="a", maxBytes=5*1024*1024, backupCount=2) -> int:
      self.logger = logging.getLogger(self.name)
      self.logger.setLevel(logging.DEBUG)

      self.stdout_formatter = logging.Formatter('%(levelname)s | %(name)s | %(message)s')
      self.file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s', '%m-%d-%Y %H:%M:%S')

      self.stdout_handler = logging.StreamHandler(sys.stdout)
      self.stdout_handler.setLevel(level_stdo)
      self.stdout_handler.setFormatter(self.stdout_formatter)
      self.logger.addHandler(self.stdout_handler)

      if self.logger_file_path:
         self.file_handler = RotatingFileHandler(self.logger_file_path, mode=mode, maxBytes=maxBytes, backupCount=backupCount)
         self.file_handler.setLevel(level_file)
         self.file_handler.setFormatter(self.file_formatter)

         self.logger.addHandler(self.file_handler)
      return 0
            
   
   def get_Logger(self) -> logging.Logger:
      return self.logger


   def set_Logger(self, logger: logging.Logger):
        self.logger = logger
    
    
   def get_Logs(self):
      root_path_log = "/".join(self.logger_file_path.split("/")[:-1])
      log_file_name = self.logger_file_path.split("/")[-1]
      return [root_path_log + "/" + i for i in list_dir(root_path_log) if log_file_name in i]
            

   def run(self) -> None:
      self.is_running = False
      self.is_finished = False
      
      while not self.is_Thread_Stopped():
         while not self.is_Task_Stopped():
            
            self.is_running = True
            self.is_finished = False
            
            response = self.task(
                  **self.get_Parameters()
            )
            
            self.is_running = False
            
            if response == 0:
               self.logger.info("Task Finished Successfully")
               self.is_finished = True
            else:
               self.logger.warning("Task Manually Stopped")
            
            self.stop_Task()
            time.sleep(1)
         time.sleep(1)


   def stop_Thread(self) -> int:
      self._flag_thread_stop = True
      self._flag_task_stop = True
      self.join()
      self.logger.warning("Thread Stopped")
      return 0


   def stop_Task(self) -> int:
      self._flag_task_stop = True
      self.logger.warning("Task Stopped")
      return 0


   def wait_To_Stop_Once_Task(self) -> int:
      self.logger.warning("Waiting to stop task once...")
      while self.is_Running():
         time.sleep(1)
      self.logger.warning("Task once stopped...")
      return 0


   def wait_To_Stop_Task(self) -> int:
      self.logger.warning("Waiting to stop task fully...")
      while self.is_Running() and self.is_Thread_Started():
         time.sleep(1)
      self.logger.warning("Task fully stopped...")
      return 0


   def is_Running(self) -> bool:
      return self.is_running
   

   def is_Thread_Stopped(self) -> bool:
      return self._flag_thread_stop


   def is_Finished(self) -> bool:
      return self.is_finished


   def is_Thread_Started(self) -> bool:
      return not self._flag_thread_stop


   def is_Task_Stopped(self) -> bool:
      return self._flag_task_stop


   def get_Parameters(self) -> dict[str, str]:
      return self.parameters.copy()


   def start_Task(self) -> int:
      if self.is_Thread_Stopped():
         self.logger.warning("Thread already stopped. Can NOT do the task!")
         return 1

      self._flag_task_stop = False
      self.logger.info("Task Started")
      return 0


   def start_Thread(self, start_task:bool=False) -> int:
      self._flag_thread_stop = False
      self.start()
      if start_task:
         self.start_Task()
      self.logger.info("Thread Started")
      return 0


   @abstractmethod
   def set_Parameters(self):
      # Re-Write set_Parameter Function to set parameters for Task Function
      raise NotImplementedError


   @abstractmethod
   def task(self):
      # Re-Write Task Function
      raise NotImplementedError
   