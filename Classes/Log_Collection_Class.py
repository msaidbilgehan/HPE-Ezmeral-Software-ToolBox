

 
from datetime import datetime
import os
import time

from Classes.Task_Handler import Task_Handler_Class
from Libraries.network_tools import ssh_execute_command, ssh_receive_file
from Libraries.tools import list_dir

class Log_Collection_Class(Task_Handler_Class):
    def __init__(self, download_path, *args, **kwargs):
        super(Log_Collection_Class, self).__init__(*args, **kwargs)
        
        self.download_path = download_path
        
        self.__parameters_template = {
            "ssh_username": "",
            "ssh_password": "",
            "ip_addresses": []
        }
        self.parameters = self.__parameters_template.copy()


    def set_Parameters(self, ssh_username: str, ssh_password: str, ip_addresses: list[str]) -> int:
        self.parameters = self.__parameters_template.copy()
        
        self.parameters["ssh_username"] = ssh_username
        self.parameters["ssh_password"] = ssh_password
        self.parameters["ip_addresses"] = ip_addresses
        return 0
   

    def task(self, ssh_username, ssh_password, ip_addresses):
        self.logger.info(f"Collecting Logs of {ip_addresses} ...")

        try:
            # Create directory of Given Path if not exists
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)
            
            # Check Thread State
            time.sleep(1)
            if self.is_Thread_Stopped():
                return -1
            
            log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            timestamp_folder_logs = self.download_path + log_timestamp + "/"
            
            # Execute cleanup.py over SSH
            for ip_address in ip_addresses:
                self.logger.info("Connecting to " + ip_address + " ...")
                
                status, client_stdout = ssh_execute_command(
                    ssh_client=ip_address, 
                    username=ssh_username, 
                    password=ssh_password, 
                    command="sudo find /opt/mapr/ -name logs",
                    reboot=False,
                    logger_hook=self.logger
                )
                
            
            # Check Thread State
                time.sleep(1)
                if self.is_Thread_Stopped():
                    return -1
                
                log_folders =  client_stdout.split("\n")
                log_folders = [log_folder for log_folder in log_folders if log_folder != ""]
                
                for log_folder in log_folders:
                    remote_file_path = ssh_receive_file(
                        ssh_client=ip_address,
                        username=ssh_username,
                        password=ssh_password,
                        remote_path=log_folder,
                        local_folder_path=timestamp_folder_logs + ip_address + "/",
                        sleep_time=0,
                        logger_hook=self.logger
                    )
                    
                    # Check Thread State
                    time.sleep(1)
                    if self.is_Thread_Stopped():
                        return -1
                    
                    if remote_file_path == "":
                        self.logger.info(f"ERROR: File transfer failed! Remote '{ip_address}' Path is '{log_folder}'")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        
        self.logger.info(f"Log Connection Finished for IP Addresses: {ip_addresses}")
        
        return 0
    
    
    def get_Collected_Log_Folder(self):
        return self.download_path
    
    
    def get_Logs(self):
        root_path_log = "/".join(self.logger_file_path.split("/")[:-1])
        log_file_name = self.logger_file_path.split("/")[-1]
        return [root_path_log + "/" + i for i in list_dir(root_path_log) if log_file_name in i]