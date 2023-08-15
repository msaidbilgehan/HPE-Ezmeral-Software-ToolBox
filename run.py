import os
from Libraries.network_tools import ping_sweeping_threaded, select_ip_addresses, ssh_send_file, ssh_execute_command, get_local_IP, scan_ip


def initialize_message():
    print('-----------------------------------')
    print('HPE Ezmeral Data Fabric ToolBox Project')
    print('Reference: https://docs.ezmeral.hpe.com/')
    print('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    print('All Rights reserved.')
    print('Version 1.11')
    print('-----------------------------------')
    print('TREO Information Technologies')
    print('https://www.treo.com.tr/')
    print('-----------------------------------')
    



def menu():
    print("1. FQDN Setup")
    print("2. Cleanup Node")
    print("3. Exit")
    option = input("Please select an option: ")
    return option



def menu_action_selection():
    option = ""
    
    while option != "3":
        option = menu()
        
        if option == "1":
            print("FQDN Setup Starting...")
            os.system("python ./FQDN_Tools/run.py")
            
        elif option == "2":
            print("Scanning the local network...")
            
            network_address = get_local_IP()
            network_address = network_address[:network_address.rfind(".")] + ".x"

            # IP Scan
            scan_result = ping_sweeping_threaded(
                network_address=input(f"Please enter a Network Address [{network_address}]: ")
            )
            if scan_result == []:
                print("No IP found in the network. Please try again.")
                continue
            
            # Select Target IP Addresses
            selected_ip_addresses = select_ip_addresses(scan_result)
            if selected_ip_addresses == []:
                print("No IP Selected!")
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
                print("Connecting to " + target["ip"] + " ...")
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
                    print("ERROR: File transfer failed!")
                    print("")
                    continue
            
        elif option == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid option. Please try again.")



if __name__ == "__main__":
    initialize_message()
    menu_action_selection()
    print("Exiting...")
    exit()