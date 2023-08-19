

from datetime import datetime
import os
import time
from FQDN_Tools.tools import get_local_IP, ping_sweeping_threaded
from Libraries.network_tools import ping_sweeping_threaded, select_ip_addresses, ssh_send_file, ssh_execute_command, get_local_IP, ssh_receive_file
from Libraries.logger_module import cleanup_logger, log_collection_logger



def fqdn_setup():
    os.system("python ./FQDN_Tools/run.py")



def cleanup():
    cleanup_logger.info("Scanning the local network...")
    network_address = get_local_IP()
    network_address = network_address[:network_address.rfind(".")] + ".x"

    # IP Scan
    scan_result = ping_sweeping_threaded(
        network_address=input(f"Please enter a Network Address [{network_address}]: "),
        logger_hook=cleanup_logger
    )
    if scan_result == []:
        cleanup_logger.warning("No IP found in the network. Please try again.")
        return -1
    
    # Select Target IP Addresses
    selected_ip_addresses = select_ip_addresses(
        scan_result,
        logger_hook=cleanup_logger
    )
    if selected_ip_addresses == []:
        cleanup_logger.warning("No IP Selected!")
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
        cleanup_logger.info("Connecting to " + target["ip"] + " ...")
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
            overwrite=True,
            logger_hook=cleanup_logger
        )
        if remote_file_path != "":
            ssh_execute_command(
                ssh_client=target["ip"], 
                username=ssh_username, 
                password=ssh_password, 
                command=f"python3 {remote_file_path} {ssh_password}",
                reboot=False,
                logger_hook=cleanup_logger
            )
        else:
            cleanup_logger.info("ERROR: File transfer failed!")
            return -1
    return 0



def log_collection(ssh_username, ssh_password, ip_addresses):
    log_collection_logger.info(f"Collecting Logs of {ip_addresses} ...")
    
    try:
        # log_collection_logger.info("Scanning the local network...")
        # time.sleep(1)  # Wait for new content
        
        # network_address = get_local_IP()
        # network_address = network_address[:network_address.rfind(".")] + ".x"

        # IP Scan
        # scan_result = ping_sweeping_threaded(
        #     network_address=network_address_mask
        # )
        # if scan_result == []:
        #     log_collection_logger.warning("No IP found in the network. Please try again.")
            # return -1
        # time.sleep(1)  # Wait for new content
        
        # Select Target IP Addresses
        # ip_addresses = select_ip_addresses(scan_result)
        # if ip_addresses == []:
        #     log_collection_logger.warning("No IP Selected!")
        #     return -1
        
        # Send Hosts File
        # ssh_username = ""
        # ssh_password = ""
        # same_ssh_information_for_all = "n"
        # if len(ip_addresses) > 1:
        #     same_ssh_information_for_all = input("Are all ssh logins have same credentials? (y/n): ")
            
        #     if same_ssh_information_for_all == "y":
        #         ssh_username = input("Please enter a Username: ")
        #         ssh_password = input("Please enter a Password: ")


        # Create directory of Given Path if not exists
        root_folder_logs = "./node_logs/"
        if not os.path.exists(root_folder_logs):
            os.makedirs(root_folder_logs)
        time.sleep(1)  # Wait for new content
        
        log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        timestamp_folder_logs = root_folder_logs + log_timestamp + "/"
        
        # Execute cleanup.py over SSH
        for ip_address in ip_addresses:
            log_collection_logger.info("Connecting to " + ip_address + " ...")
            
            # if same_ssh_information_for_all == "n":
            #     ssh_username = input("Please enter a Username: ")
            #     ssh_password = input("Please enter a Password: ")
            
            status, client_stdout = ssh_execute_command(
                ssh_client=ip_address, 
                username=ssh_username, 
                password=ssh_password, 
                command="sudo find /opt/mapr/ -name logs",
                reboot=False,
                logger_hook=log_collection_logger
            )
            time.sleep(1)  # Wait for new content
            
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
                    ssh_client=ip_address,
                    username=ssh_username,
                    password=ssh_password,
                    remote_path=log_folder,
                    local_folder_path=timestamp_folder_logs + ip_address + "/",
                    sleep_time=0,
                    logger_hook=log_collection_logger
                )
                time.sleep(1)  # Wait for new content
                if remote_file_path == "":
                    log_collection_logger.info(f"ERROR: File transfer failed! Remote '{ip_address}' Path is '{log_folder}'")
                    # return -1
    except Exception as e:
        log_collection_logger.error(f"An error occurred: {e}")
    