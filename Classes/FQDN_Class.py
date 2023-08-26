

 
import time

from Classes.Task_Handler import Task_Handler_Class
from Libraries.network_tools import create_hosts_file, send_hostfile_to_device_ssh, update_hostname_ssh



class FQDN_Class(Task_Handler_Class):
    def __init__(self, *args, **kwargs):
        super(FQDN_Class, self).__init__(*args, **kwargs)
        
        self.__parameters_template:dict[str, str | list[dict[str, str]]] = {
            "ssh_username": "",
            "ssh_password": "",
            "ip_address_hostname_list": [],
        }
        self.parameters = self.__parameters_template.copy()


    def set_Parameters(self, ssh_username: str, ssh_password: str, ip_address_hostname_list: list[dict[str, str]]) -> int:
        self.parameters = self.__parameters_template.copy()
        
        self.parameters["ssh_username"] = ssh_username
        self.parameters["ssh_password"] = ssh_password
        self.parameters["ip_address_hostname_list"] = ip_address_hostname_list
        return 0
   

    def task(self, ssh_username, ssh_password, ip_address_hostname_list):
        self.logger.info(f"Cleaning {ip_address_hostname_list} ...")
        
        failed_ip_addresses:list[dict[str, str]] = list()

        try:
            # Check Thread State
            time.sleep(1)
            if self.is_Thread_Stopped():
                return -1
            
            # Create Hosts File
            ip_address_hostname_list = create_hosts_file(
                ip_address_hostname_list=ip_address_hostname_list,
                logger_hook=self.logger
            )
            
            # Check Thread State
            time.sleep(1)
            if self.is_Thread_Stopped():
                return -1
            
            # Execute cleanup.py over SSH
            for i, ip_address_hostname in enumerate(ip_address_hostname_list):
                self.logger.info(f"Connecting to {ip_address_hostname} ...")
                filepath_for_ip_address =  f"hosts_{ip_address_hostname['ip']}"
                
                response = send_hostfile_to_device_ssh(
                    ip_address=ip_address_hostname["ip"], 
                    username=ssh_username, 
                    password=ssh_password, 
                    local_file_path=filepath_for_ip_address,
                    remote_file_path="/etc/hosts", 
                )
                if response != 0:
                    failed_ip_addresses.append(ip_address_hostname)
                    continue
            
                # Check Thread State
                time.sleep(1)
                if self.is_Thread_Stopped():
                    return -1
                
                response = update_hostname_ssh(
                    ip_address=ip_address_hostname["ip"], 
                    # port=int(input("Please enter a Port: ")), 
                    username=ssh_username, 
                    password=ssh_password, 
                    new_hostname=ip_address_hostname_list[i]["hostname"],
                    reboot="y"
                )
                if response != 0:
                    failed_ip_addresses.append(ip_address_hostname)
                
                # Check Thread State
                time.sleep(1)
                if self.is_Thread_Stopped():
                    return -1
                    
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        
        if len(failed_ip_addresses) > 0:
            self.logger.info(f"Cleanup Failed for IP Addresses: {failed_ip_addresses}")
        self.logger.info(f"Cleanup Finished for IP Addresses: {[ip_hostname for ip_hostname in ip_address_hostname_list if ip_hostname not in failed_ip_addresses]}")
        
        return 0