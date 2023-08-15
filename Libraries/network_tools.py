import os
from socket import socket, AF_INET, SOCK_STREAM, gethostbyaddr, gethostbyname, gethostname
import concurrent.futures
import paramiko



def ssh_send_file(ssh_client:str, username:str, password:str, local_file_path:str, remote_file_path:str="/tmp/", port:int=22, overwrite=False):
    transport = paramiko.Transport((ssh_client, port))
    
    remote_file_path = remote_file_path if remote_file_path[-1] == "/" else remote_file_path + "/"
    remote_tmp_path = "/tmp/" + os.path.basename(local_file_path)
    uploaded_location = remote_file_path + os.path.basename(local_file_path)
    
    response_upload = False
    response_command = False
    
    try:
        if overwrite:
            # Delete file if exists
            print(f"Deleting file {remote_tmp_path}...")
            response_command = ssh_execute_command(
                ssh_client=ssh_client, 
                username=username, 
                password=password, 
                command=f'sudo rm -f {remote_tmp_path}', 
                port=port, 
                reboot=False
            )
            if response_command == False:
                raise Exception("Error deleting file")
        
        transport.connect(username=username, password=password)
        sftp = transport.open_sftp_client()

        if sftp is None:
            raise Exception("Error opening SFTP Client")

        print(f"Uploading file to {remote_tmp_path}...")
        # upload file to temporary location
        sftp.put(local_file_path, remote_tmp_path)
        sftp.close()
        response_upload = True
        
        if remote_tmp_path != uploaded_location:
            if overwrite:
                print(f"Deleting file {uploaded_location}...")
                response_command = ssh_execute_command(
                    ssh_client=ssh_client, 
                    username=username, 
                    password=password, 
                    command=f'sudo rm -f {uploaded_location}', 
                    port=port, 
                    reboot=False
                )
            print(f"Moving file to {uploaded_location}...")
            # Move file to the desired location
            response_command = ssh_execute_command(
                ssh_client=ssh_client, 
                username=username, 
                password=password, 
                command=f'sudo mv {remote_tmp_path} {uploaded_location}', 
                port=port, 
                reboot=False
            )
            if response_command == False:
                raise Exception("Error moving file to desired location")

    except paramiko.AuthenticationException:
        print("Authentication failed")
        uploaded_location = ""
    except Exception as e:
        print("Exception: ", e)
        if response_upload == False and response_command == False:
            uploaded_location = ""
        elif response_upload == True and response_command == False:
            uploaded_location = uploaded_location
    finally:
        transport.close()

    return uploaded_location



def ssh_execute_command(ssh_client:str, username:str, password:str, command:str, port:int=22, is_sudo=False, reboot:bool=False):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    status = False
    
    try:
        client.connect(ssh_client, port, username, password)
        print("Connection Established!")
        
        # update hostname
        # stdin, stdout, stderr = client.exec_command(f'echo {new_hostname} > /etc/hostname')
        if is_sudo:
            command = f'echo {password} | {command}'
            # command = f'echo {password} | sudo -S sh -c "echo \'{command}\'"'
        
        print("Executing command: ", command)
        stdin, stdout, stderr = client.exec_command(command)
        # print("stdout:", stdout.read().decode())
        
        exit_status = stdout.channel.recv_exit_status() # Blocking call
        if exit_status==0:
            print("Command successfully executed!")
            status = True
            
            if reboot:
                stdin_reboot, stdout_reboot, stderr_reboot = client.exec_command('echo {password} | sudo reboot -h now')
            else:
                print("Reboot skipped.")
        else:
            print("Error", exit_status)
            print("Detail:", stdout.read().decode())
            print("Error Detail:", stderr.read().decode())
            status = False
        
    except paramiko.AuthenticationException:
        print("Authentication failed")
        status = False
    finally:
        client.close()
        
    return status
    


def get_local_IP():
    return gethostbyname(gethostname())



def ping_by_ip(ip_address: str, legacy=False, port=22)-> bool:
    if legacy:
        os_type = os.name

        if os_type == "nt":  # Windows
            ping_command = "ping -n 1 "
        else:  # Assume Linux or macOS
            ping_command = "ping -c 1 "

        command = ping_command + ip_address
        response = os.popen(command)

        print("Response: ", response.readlines())

        for line in response.readlines():
            if "TTL" in line:
                # print(ip_address, "--> Live")
                return True

        return False
    else:
        # Check if the IP is reachable
        port, is_open = scan_port(ip_address, port=port)
        return is_open

      

# define the function to scan a single port
def scan_port(ip_address:str, port:int):
    # sock = socket(AF_INET, SOCK_STREAM)
    # sock.settimeout(3)  # Set a timeout of 3 second
    # is_open = False
    # try:
    #     conn = sock.connect_ex((ip_address, port))
    #     if conn == 0:
    #         # print(f'Port {port}: OPEN')
    #         is_open = True
    # finally:
    #     sock.close()
    
    is_open = False
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(3)  # Set a timeout of 3 second
        try:
            conn = sock.connect_ex((ip_address, port))
            if conn == 0:
                # print(f'Port {port}: OPEN')
                is_open = True
        except:
            pass
    
    return port, is_open


def get_hostname_by_ip(ip_address:str):
    try:
        return gethostbyaddr(ip_address)[0]
    except:
        return None



def scan_ip(scan_ip_address):
    response = ping_by_ip(scan_ip_address)

    if response == False:
        return None

    hostname = get_hostname_by_ip(scan_ip_address)

    # if hostname:
    #     print(f"IP: {scan_ip_address}, Hostname: {hostname}")
    # else:
    #     print(f"IP: {scan_ip_address}")
        
    dict_ip_hostname_template = {
        "ip": "",
        "hostname": ""
    }

    entry = dict_ip_hostname_template.copy()
    entry["ip"] = scan_ip_address
    entry["hostname"] = hostname if hostname else ""
    return entry

    
    
def ping_sweeping_threaded(network_address:str, start:int=1, end:int=255)->list:
    if network_address == "":
        network_address = get_local_IP()
        network_address = network_address[:network_address.rfind(".")] + ".x"
        print("Selected Default IP Mask:", network_address)
    
    network_address_splitted= network_address.split('.')
    last_dot = '.'

    network_address_clean = network_address_splitted[0] + last_dot + network_address_splitted[1] + last_dot + network_address_splitted[2] + last_dot

    list_ip_hostname = []

    print(f"Starting to scan.")
    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        futures = []
        for i in range(start, end):
            scan_ip_address = network_address_clean + str(i)
            futures.append(executor.submit(scan_ip, scan_ip_address))

        print(f"Scanning...")
        for future in concurrent.futures.as_completed(futures):
            entry = future.result()
            if entry is not None:
                list_ip_hostname.append(entry)
            
    # Sort the list by IP address
    list_ip_hostname = sorted(list_ip_hostname, key=lambda x: tuple(map(int, x['ip'].split('.'))))

    print(f"Scanning completed.")
    print("")
    
    return list_ip_hostname


    
def select_ip_addresses(ip_addresses:list)->list:
    selected_ip_addresses = []
    
    print("Select IP Addresses to connect over ssh:")
    print_ip_table(ip_hostname_pack=ip_addresses)

    selected_indexes = input("Please enter the IP Addresses to add to the Hosts File (separated by comma)[1,2,3]: ")
    selected_indexes = selected_indexes.split(",")
    selected_indexes = list(map(str.strip, selected_indexes))
    selected_indexes = [int(index) for index in selected_indexes if index != "" or index.isdigit()]

    for index in selected_indexes:
        selected_ip_addresses.append(ip_addresses[index])
    
    return selected_ip_addresses



def print_ip_table(ip_hostname_pack):
    print(f"\tIP\t |\tHostname")
    for i, result in enumerate(ip_hostname_pack):
        print(f" ({i})\t{result['ip']}\t |\t {result['hostname'] if result['hostname'] else '---'}")