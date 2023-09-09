

 
import time

from Flask_App.Classes.Task_Handler import Task_Handler_Class
from Flask_App.Libraries.network_tools import ssh_execute_command, ssh_send_file



class Backup_Class(Task_Handler_Class):
    def __init__(self, *args, **kwargs):
        super(Backup_Class, self).__init__(*args, **kwargs)
        
        self.__parameters_template = {
            "ssh_username": "",
            "ssh_password": "",
            "ip_addresses": [],
            "script_path": "",
            "script_upload_path": "",
            "script_run_command": "",
            "script_parameters": "",
            "cron_parameters": "",
            "add_to_cron": False,
        }
        self.parameters = self.__parameters_template.copy()


    def set_Parameters(self, script_path: str, script_upload_path:str, script_run_command:str, script_parameters:str, add_to_cron: bool, cron_parameters:str, ssh_username: str, ssh_password: str, ip_addresses: list[str]) -> int:
        self.parameters = self.__parameters_template.copy()
        
        self.parameters["ssh_username"] = ssh_username
        self.parameters["ssh_password"] = ssh_password
        self.parameters["ip_addresses"] = ip_addresses
        self.parameters["script_path"] = script_path
        self.parameters["script_upload_path"] = script_upload_path
        self.parameters["script_run_command"] = script_run_command
        self.parameters["script_parameters"] = script_parameters
        self.parameters["add_to_cron"] = add_to_cron
        self.parameters["cron_parameters"] = cron_parameters
        return 0
   

    def task(self, script_path:str, script_upload_path:str, script_run_command:str, script_parameters:str, add_to_cron: bool, cron_parameters:str, ssh_username:str, ssh_password:str, ip_addresses:list[str]) -> int:
        self.logger.info(f"Backup Job Adding to {ip_addresses} ...")
        
        failed_ip_addresses:list[str] = list()

        try:
            # Check Thread State
            time.sleep(1)
            if self.stop_Action_Control():
                self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                return -1
            
            # Execute script over SSH
            # Send backup script to remote devices
            for ip_address in ip_addresses:
                self.logger.info("Connecting to " + ip_address + " ...")
                
                remote_file_path = ssh_send_file(
                    ssh_client=ip_address, 
                    username=ssh_username, 
                    password=ssh_password, 
                    local_file_path=script_path,
                    remote_file_path=script_upload_path, 
                    overwrite=True,
                    logger_hook=self.logger
                )

                # Check Thread State
                time.sleep(1)
                if self.stop_Action_Control():
                    self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                    return -1
                
                if remote_file_path != "":
        
                    # If run command given, execute it
                    if script_run_command != "":
                        ssh_command = f"{script_run_command} {remote_file_path} {script_parameters}"
                        
                        ssh_execute_command(
                            ssh_client=ip_address, 
                            username=ssh_username, 
                            password=ssh_password, 
                            command=ssh_command,
                            reboot=False,
                            logger_hook=self.logger
                        )
                        
                    if add_to_cron:
                        if cron_parameters == "":
                            hour = "0"
                            minute = "0"
                            month = "*"
                            day_of_month = "*"
                            day_of_week = "*"
                        else:
                            hour, minute, month, day_of_month, day_of_week = cron_parameters.split(" ")
                        
                        ssh_command = f"echo '{hour} {minute} {month} {day_of_month} {day_of_week} {remote_file_path}' | crontab -l - | crontab -"
                        
                        response, stout = ssh_execute_command(
                            ssh_client=ip_address, 
                            username=ssh_username, 
                            password=ssh_password, 
                            command=ssh_command,
                            reboot=False,
                            logger_hook=self.logger
                        )
                        if response != 0:
                            self.logger.warn(f"Cron adding failed -> {ip_address}")
                            self.logger.warn(f"{ip_address} :: {stout}")
                            failed_ip_addresses.append(ip_address)
                else:
                    self.logger.info(f"File transfer failed -> {ip_address}")
                    failed_ip_addresses.append(ip_address)
                
                # Check Thread State
                time.sleep(1)
                if self.stop_Action_Control():
                    self.logger.warn("Thread Task Forced to Stop. Some actions may have done before stop, be carefully continue.")
                    return -1
                    
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        
        if len(failed_ip_addresses) > 0:
            self.logger.info(f"Backup Failed for IP Addresses: {failed_ip_addresses}")
        self.logger.info(f"Backup Finished for IP Addresses: {[ip for ip in ip_addresses if ip not in failed_ip_addresses]}")
        
        return 0