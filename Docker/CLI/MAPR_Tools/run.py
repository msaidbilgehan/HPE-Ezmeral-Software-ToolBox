


import os
import socket



def initialize_message():
    print('-----------------------------------')
    print('TREO Information Technologies')
    print('https://www.treo.com.tr/')
    print('-----------------------------------')
    print('Node Installation Script')
    print('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    print('All Rights reserved.')
    print('Version 1.11')
    print('-----------------------------------')
    



def menu():
    print("IP Address: " + get_ip_address())
    print("1. Install Node (All)")
    print("2. Install Node (Dependencies)")
    print("3. Cleanup Node")
    print("4. Exit")
    print("Please select an option: ", end="")
    option = input()
    return option



def menu_action_selection():
    option = menu()
    
    commands = {
        "1": "sudo python3 ./prepare_setup.py",
        "2": "sudo python3 ./setup_dependencies.py",
        "3": "sudo python3 ./cleanup.py",
        "4": "exit",
    }
    
    if option == "1":
        print("Installing Node (All)...")
    elif option == "2":
        print("Installing Node (Dependencies)...")
    elif option == "3":
        print("Cleaning up...")
    elif option == "4":
        print("Exiting...")
        exit()
    else:
        print("Invalid option. Please try again.")
        menu_action_selection()

    run_setup_script(command=commands[option])



def run_setup_script(command):
    os.system(command)



def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


if __name__ == "__main__":
    initialize_message()
    menu_action_selection()
    print("Exiting...")
    exit()