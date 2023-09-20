

 
from datetime import datetime
import os
import time

from Flask_App.Classes.Task_Handler import Task_Handler_Class
from Flask_App.Libraries.network_tools import ssh_execute_command, ssh_receive_file



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
        failed_ip_addresses:list[str] = list()

        try:
            # Create directory of Given Path if not exists
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)
            
            # Check Thread State
            time.sleep(1)
            if self.stop_Action_Control():
                self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                return -1
            
            log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            timestamp_folder_logs = self.download_path + log_timestamp + "/"
            
            # Execute cleanup.py over SSH
            for ip_address in ip_addresses:
            
                # Check Thread State
                time.sleep(1)
                if self.stop_Action_Control():
                    self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                    return -1
                
                self.logger.info("Connecting to " + ip_address + " ...")
                
                connection, status, client_stdout = ssh_execute_command(
                    ssh_client=ip_address, 
                    username=ssh_username, 
                    password=ssh_password, 
                    command="sudo find /opt/mapr/ -name logs",
                    reboot=False,
                    logger_hook=self.logger
                )
                if not status or not connection:
                    failed_ip_addresses.append(ip_address)
                    self.logger.error(f"Failed to run command in client: '{ip_address}''")
                    continue
                
                log_folders =  client_stdout.split("\n")
                log_folders = [log_folder for log_folder in log_folders if log_folder != ""]
                
                for log_folder in log_folders:
                    connection, file_transfer, remote_file_path = ssh_receive_file(
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
                    if self.stop_Action_Control():
                        self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                        return -1
                    
                    if not file_transfer:
                        self.logger.error(f"File transfer failed! Remote '{ip_address}' Path is '{log_folder}'. Response: {remote_file_path}")
                        failed_ip_addresses.append(ip_address)
                        continue
                    
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        
        if len(failed_ip_addresses) > 0:
            self.logger.info(f"Log Collection Task Failed for IP Addresses: {failed_ip_addresses}")
        self.logger.info(f"Log Collection Task Finished for IP Addresses: {[ip for ip in ip_addresses if ip not in failed_ip_addresses]}")
        
        return 0


    def get_Collected_Log_Folder(self):
        return self.download_path
    