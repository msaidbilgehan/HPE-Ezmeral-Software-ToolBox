from tools import port_scanner, get_ip_by_hostname, get_hostname_by_ip, ping_sweeping_threaded, save_to_json, load_from_json, update_hostname_ssh, create_hosts_file, print_ip_table, send_hostfile_to_device_ssh, get_local_IP



def initialize_message():
    print('')
    print('.-------------------------------------.')
    print('| Welcome to the Network Scanner Tool |')
    print('|  Written by Muhammed Said BİLGEHAN  |')
    print('\'-------------------------------------\'')
    print('')
    print("IP Address:", get_local_IP())
    print('')
    
def print_menu_actions():
    # print("0. Print This Menu")
    
    print("1. Ping Sweeping")
    print("2. Port Scanning")
    
    print("3. Get IP Address by Hostname")
    print("4. Get Hostname by IP Address")

    print("5. Rename Hostname")
    print("6. Create Hosts File")
    print("7. Sync Hosts File with Specified Hosts")
    print("8. Automate - Create Hosts File and Sync Hosts File with Specified Hosts")
    
    print("9. Exit")
    
def select_ip_addresses_from_json()->list:
    selected_ip_addresses = []
    
    print("Loading IP-Hostname Dictionary from JSON file...")
    ip_addresses = load_from_json(path="results.json")
    if ip_addresses == None:
        print("No IP-Hostname Dictionary found!")
        return selected_ip_addresses
    
    print("Select IP Addresses to add to the Hosts File: ")
    print_ip_table(ip_hostname_dict=ip_addresses)

    selected_indexes = input("Please enter the IP Addresses to add to the Hosts File (separated by comma)[1,2,3]: ")
    selected_indexes = selected_indexes.split(",")
    selected_indexes = list(map(str.strip, selected_indexes))
    selected_indexes = [int(index) for index in selected_indexes if index != "" or index.isdigit()]

    for index in selected_indexes:
        selected_ip_addresses.append(ip_addresses[index])
    
    return selected_ip_addresses
    
    
def menu_action_selection():

    option = "-1"
    
    while option not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print_menu_actions()
        print("Please select an option: ", end="")
        option = input()
        
        # if option == "0":
        #     print_menu_actions()

        if option == "1":
            # ping_sweeping(network_address=input("Please enter a Network Address: "))
            local_ip_mask = get_local_IP()
            local_ip_mask = local_ip_mask[:local_ip_mask.rfind(".")] + ".x"
            scan_result = ping_sweeping_threaded(network_address=input(f"Please enter a Network Address [{local_ip_mask}]: "))
            if scan_result == []:
                continue
            
            print_ip_table(ip_hostname_dict=scan_result)
            
            print("\nTotal Results: " + str(len(scan_result)))
            
            print("Do you want to save the result to a JSON file? (y/n): ", end="")
            save_option = input()
            if save_option == "y":
                save_to_json(data=scan_result, path="results.json")
                
        elif option == "2":
            port_scanner(
                ip_address=input("Please enter an IP Address: ")
            )
        elif option == "3":
            print("IP Address:", get_ip_by_hostname(hostname=input("Please enter a Hostname: ")))
        elif option == "4":
            print("Hostname:", get_hostname_by_ip(ip_address=input("Please enter an IP Address: ")))
        elif option == "5":
            update_hostname_ssh(
                ip_address=input("Please enter an IP Address: "), 
                # port=int(input("Please enter a Port: ")), 
                username=input("Please enter a Username: "), 
                password=input("Please enter a Password: "), 
                new_hostname=input("Please enter a New Hostname: "),
                reboot=input("Do you want to reboot the device? (y/n): ")
            )
        elif option == "6":
            selected_ip_addresses = select_ip_addresses_from_json()
            if selected_ip_addresses == []:
                print("No IP Selected!")
                continue
                
            ip_address_hostname_list = create_hosts_file(ip_address_hostname_list=selected_ip_addresses)
            
            print("Do you want to save the IP Addresses to a JSON file? (y/n): ", end="")
            save_option = input()
            if save_option == "y":
                save_to_json(data=ip_address_hostname_list, path="selected_ip_addresses.json")

        elif option == "7":
            
            print("Do you want to load the IP Addresses from the JSON file? (y/n): ", end="")
            load_option = input()
            if load_option == "y":
                target_ip_addresses = load_from_json(path="selected_ip_addresses.json")
                if target_ip_addresses == None:
                    print("No IP Addresses found!")
                    continue
            else:
                target_ip_addresses = select_ip_addresses_from_json()
                if target_ip_addresses == []:
                    print("No IP Selected!")
                    continue
            
            for target in target_ip_addresses:
                print("Sending Hosts File to " + target["ip"] + "...")
                filepath_for_ip_address =  "hosts_" + target["ip"]
                
                send_hostfile_to_device_ssh(
                    ip_address=target["ip"], 
                    username=input("Please enter a Username: "), 
                    password=input("Please enter a Password: "), 
                    local_file_path=filepath_for_ip_address,
                    remote_file_path="/etc/hosts", 
                )
            
        elif option == "8":
            # IP Scan
            scan_result = ping_sweeping_threaded(
                network_address=input("Please enter a Network Address [10.34.2.x]: ")
            )
            if scan_result == []:
                continue
            
            # Save IP Scan Result
            save_to_json(data=scan_result, path="results.json")
            
            # Select Target IP Addresses
            selected_ip_addresses = select_ip_addresses_from_json()
            if selected_ip_addresses == []:
                print("No IP Selected!")
                continue
                
            # Create Hosts File
            ip_address_hostname_list = create_hosts_file(ip_address_hostname_list=selected_ip_addresses)
            
            # Send Hosts File
            
            same_ssh_information_for_all = input("Are all ssh logins have same credentials? (y/n): ")
            
            ssh_username = ""
            ssh_password = ""
            if same_ssh_information_for_all == "y":
                ssh_username = input("Please enter a Username: ")
                ssh_password = input("Please enter a Password: ")
                
            
            for i, target in enumerate(selected_ip_addresses):
                print("Sending Hosts File to " + target["ip"] + "...")
                filepath_for_ip_address =  "hosts_" + target["ip"]
                
                if same_ssh_information_for_all != "y":
                    ssh_username = input("Please enter a Username: ")
                    ssh_password = input("Please enter a Password: ")
                
                send_hostfile_to_device_ssh(
                    ip_address=target["ip"], 
                    username=ssh_username, 
                    password=ssh_password, 
                    local_file_path=filepath_for_ip_address,
                    remote_file_path="/etc/hosts", 
                )
                update_hostname_ssh(
                    ip_address=target["ip"], 
                    # port=int(input("Please enter a Port: ")), 
                    username=ssh_username, 
                    password=ssh_password, 
                    new_hostname=ip_address_hostname_list[i]["hostname"],
                    reboot="y"
                )
            
            
        elif option == "9":
            break
        
    

if __name__ == "__main__":
    initialize_message()
    menu_action_selection()
    
    print("Exiting...")
    exit()