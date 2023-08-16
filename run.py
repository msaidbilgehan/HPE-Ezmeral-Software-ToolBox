from datetime import datetime
import os
from Libraries.network_tools import ping_sweeping_threaded, select_ip_addresses, ssh_send_file, ssh_execute_command, get_local_IP, ssh_receive_file
from Libraries.logger_module import logger


def initialize_message():
    logger.info('-----------------------------------')
    logger.info('HPE Ezmeral Data Fabric ToolBox Project')
    logger.info('Reference: https://docs.ezmeral.hpe.com/')
    logger.info('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    logger.info('All Rights reserved.')
    logger.info('Version 1.11')
    logger.info('-----------------------------------')
    logger.info('TREO Information Technologies')
    logger.info('https://www.treo.com.tr/')
    logger.info('-----------------------------------')
    



def menu():
    logger.info("1. FQDN Setup")
    logger.info("2. Cleanup Node")
    logger.info("3. Log Collection")
    logger.info("4. Exit")
    option = input("Please select an option: ")
    return option



def menu_action_selection():
    option = ""
    
    while option != "4":
        option = menu()
        
        if option == "1":
            logger.info("FQDN Setup Starting...")
            os.system("python ./FQDN_Tools/run.py")
            
        elif option == "2":
            logger.info("Cleanup Starting...")
            logger.info("Scanning the local network...")
            
            network_address = get_local_IP()
            network_address = network_address[:network_address.rfind(".")] + ".x"

            # IP Scan
            scan_result = ping_sweeping_threaded(
                network_address=input(f"Please enter a Network Address [{network_address}]: ")
            )
            if scan_result == []:
                logger.warning("No IP found in the network. Please try again.")
                continue
            
            # Select Target IP Addresses
            selected_ip_addresses = select_ip_addresses(scan_result)
            if selected_ip_addresses == []:
                logger.warning("No IP Selected!")
                continue
            
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
                    continue
            
        elif option == "3":
            logger.info("Collecting logs from nodes...")
            logger.info("Scanning the local network...")
            
            network_address = get_local_IP()
            network_address = network_address[:network_address.rfind(".")] + ".x"

            # IP Scan
            scan_result = ping_sweeping_threaded(
                network_address=input(f"Please enter a Network Address [{network_address}]: ")
            )
            if scan_result == []:
                logger.warning("No IP found in the network. Please try again.")
                continue
            
            # Select Target IP Addresses
            selected_ip_addresses = select_ip_addresses(scan_result)
            if selected_ip_addresses == []:
                logger.warning("No IP Selected!")
                continue
            
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
                        continue
            
        elif option == "4":
            logger.info("Exiting...")
            exit()
        else:
            logger.warning("Invalid option. Please try again.")



if __name__ == "__main__":
    initialize_message()
    menu_action_selection()
    logger.info("Exiting...")
    exit()