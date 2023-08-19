

from datetime import datetime
import os
from FQDN_Tools.tools import get_local_IP, ping_sweeping_threaded
from Libraries.network_tools import ping_sweeping_threaded, select_ip_addresses, ssh_send_file, ssh_execute_command, get_local_IP, ssh_receive_file
from Libraries.logger_module import logger



def fqdn_setup():
    os.system("python ./FQDN_Tools/run.py")



def cleanup():
    logger.info("Scanning the local network...")
    network_address = get_local_IP()
    network_address = network_address[:network_address.rfind(".")] + ".x"

    # IP Scan
    scan_result = ping_sweeping_threaded(
        network_address=input(f"Please enter a Network Address [{network_address}]: ")
    )
    if scan_result == []:
        logger.warning("No IP found in the network. Please try again.")
        return -1
    
    # Select Target IP Addresses
    selected_ip_addresses = select_ip_addresses(scan_result)
    if selected_ip_addresses == []:
        logger.warning("No IP Selected!")
        return -1
    
    # Send Hosts File
    ssh_username = ""
    ssh_password = ""
    same_ssh_information_for_all = "n"
    if len(selected_ip_addresses) > 1:
        same_ssh_information_for_all = input("Are all ssh logins have same credentials? (y/n): ")
        
        if same_ssh_information_for_all == "y":
            ssh_username = input("Please enter a Username: ")
            ssh_password = input("Please enter a Password: ")

    # Execute cleanup.py over SSH                
    for _, target in enumerate(selected_ip_addresses):
        logger.info("Connecting to " + target["ip"] + " ...")
        filepath =  "./MAPR_Tools/cleanup.py"
        
        if same_ssh_information_for_all == "n":
            ssh_username = input("Please enter a Username: ")
            ssh_password = input("Please enter a Password: ")
        
        remote_file_path = ssh_send_file(
            ssh_client=target["ip"], 
            username=ssh_username, 
            password=ssh_password, 
            local_file_path=filepath,
            # remote_file_path="/tmp/", 
            overwrite=True
        )
        if remote_file_path != "":
            ssh_execute_command(
                ssh_client=target["ip"], 
                username=ssh_username, 
                password=ssh_password, 
                command=f"python3 {remote_file_path} {ssh_password}",
                reboot=False
            )
        else:
            logger.info("ERROR: File transfer failed!")
            return -1
    return 0


def log_collection():
    logger.info("Scanning the local network...")
            
    network_address = get_local_IP()
    network_address = network_address[:network_address.rfind(".")] + ".x"

    # IP Scan
    scan_result = ping_sweeping_threaded(
        network_address=input(f"Please enter a Network Address [{network_address}]: ")
    )
    if scan_result == []:
        logger.warning("No IP found in the network. Please try again.")
        return -1
    
    # Select Target IP Addresses
    selected_ip_addresses = select_ip_addresses(scan_result)
    if selected_ip_addresses == []:
        logger.warning("No IP Selected!")
        return -1
    
    # Send Hosts File
    ssh_username = ""
    ssh_password = ""
    same_ssh_information_for_all = "n"
    if len(selected_ip_addresses) > 1:
        same_ssh_information_for_all = input("Are all ssh logins have same credentials? (y/n): ")
        
        if same_ssh_information_for_all == "y":
            ssh_username = input("Please enter a Username: ")
            ssh_password = input("Please enter a Password: ")


    # Create directory of Given Path if not exists
    root_folder_logs = "./node_logs/"
    if not os.path.exists(root_folder_logs):
        os.makedirs(root_folder_logs)
    
    log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    timestamp_folder_logs = root_folder_logs + log_timestamp + "/"
        
    # Execute cleanup.py over SSH                
    for _, target in enumerate(selected_ip_addresses):
        logger.info("Connecting to " + target["ip"] + " ...")
        
        if same_ssh_information_for_all == "n":
            ssh_username = input("Please enter a Username: ")
            ssh_password = input("Please enter a Password: ")
        
        status, client_stdout = ssh_execute_command(
            ssh_client=target["ip"], 
            username=ssh_username, 
            password=ssh_password, 
            command="sudo find /opt/mapr/ -name logs",
            reboot=False
        )
        
        log_folders =  client_stdout.split("\n")
        log_folders = [log_folder for log_folder in log_folders if log_folder != ""]
        
        # print("client_stdout", client_stdout)
        # print("log_folders", log_folders)
        
        for log_folder in log_folders:

            # # Re-Format given directory path to include the name of the client and the current date and time
            # local_folder_path += ssh_client + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "/"
            
            # # Create directory of Client if not exists
            # if not os.path.exists(local_folder_path):
            #     os.makedirs(local_folder_path)
            remote_file_path = ssh_receive_file(
                ssh_client=target["ip"],
                username=ssh_username,
                password=ssh_password,
                remote_path=log_folder,
                local_folder_path=timestamp_folder_logs + target["ip"] + "/",
            )
            if remote_file_path == "":
                logger.info(f"ERROR: File transfer failed! Remote '{target['ip']}' Path is '{log_folder}'")
                return -1
    