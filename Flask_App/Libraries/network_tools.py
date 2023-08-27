import os
from socket import socket, AF_INET, SOCK_STREAM, gethostbyaddr, gethostbyname, gethostname
import concurrent.futures
import time
from typing import Dict, List
import paramiko
from stat import S_ISDIR

from Flask_App.Libraries.logger_module import logger



def isdir(st_mode):
  try:
    return S_ISDIR(st_mode)
  except IOError:
    #Path does not exist, so by definition not a directory
    return False



def ssh_send_file(ssh_client:str, username:str, password:str, local_file_path:str, remote_file_path:str="/tmp/", port:int=22, overwrite=False, logger_hook=None) -> str:
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
    
    try:
        transport = paramiko.Transport((ssh_client, port))
    except Exception as error:
        local_logger.error(f"Error creating Transport: {error}")
        return ""
    
    remote_file_path = remote_file_path if remote_file_path[-1] == "/" else remote_file_path + "/"
    remote_tmp_path = "/tmp/" + os.path.basename(local_file_path)
    uploaded_location = remote_file_path + os.path.basename(local_file_path)
    
    response_upload = False
    response_command = False
    
    try:
        if overwrite:
            # Delete file if exists
            local_logger.info(f"Deleting file {remote_tmp_path}...")
            # print(f"Deleting file {remote_tmp_path}...")
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

        local_logger.info(f"Uploading file to {remote_tmp_path}...")
        # upload file to temporary location
        sftp.put(local_file_path, remote_tmp_path)
        sftp.close()
        response_upload = True
        
        if remote_tmp_path != uploaded_location:
            if overwrite:
                local_logger.info(f"Deleting file {uploaded_location}...")
                response_command = ssh_execute_command(
                    ssh_client=ssh_client, 
                    username=username, 
                    password=password, 
                    command=f'sudo rm -f {uploaded_location}', 
                    port=port, 
                    reboot=False
                )
            local_logger.info(f"Moving file to {uploaded_location}...")
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
        local_logger.error("Authentication failed")
        uploaded_location = ""
    except Exception as e:
        local_logger.error(f"Exception: {e}")
        if response_upload == False and response_command == False:
            uploaded_location = ""
        elif response_upload == True and response_command == False:
            uploaded_location = uploaded_location
    finally:
        transport.close()

    return uploaded_location



def ssh_receive_file(ssh_client:str, username:str, password:str, remote_path:str, local_folder_path:str="./received_files", port:int=22, sleep_time=0, logger_hook=None) -> str:
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    local_folder_path = local_folder_path if local_folder_path[-1] == "/" else local_folder_path + "/"
    
    # Create directory of Given Path if not exists
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    
    if sleep_time:
        time.sleep(sleep_time)
    
    last_download_path = ""
    response_download = False
    
    
    try:
        transport = paramiko.Transport((ssh_client, port))
    except Exception as error:
        local_logger.error(f"Error creating Transport: {error}")
        return ""
    
    try:
        transport.connect(username=username, password=password)
        sftp = transport.open_sftp_client()

        if sftp is None:
            raise Exception("Error opening SFTP Client")
    
        if sleep_time:
            time.sleep(sleep_time)

        try:
            st_mode = sftp.stat(remote_path).st_mode
            if isdir(st_mode):
                local_logger.info(f"Downloading folder from {remote_path} to {local_folder_path}...")
                local_logger.info(f"Listing directories of '{remote_path}'")

                folder_path_cache = [remote_path]
                while len(folder_path_cache) > 0:
    
                    if sleep_time:
                        time.sleep(sleep_time)
                    folder_path = folder_path_cache.pop(0)
                    r_paths = sftp.listdir(folder_path)
                    
                    for r_path in r_paths:
                        remote_path_cache = folder_path + "/" + r_path
    
                        if sleep_time:
                            time.sleep(sleep_time)

                        if isdir(sftp.stat(remote_path_cache).st_mode):
                            folder_path_cache.append(remote_path_cache)
                        else:
                            print("Creating dirs:", local_folder_path + folder_path)
                            os.makedirs(local_folder_path + folder_path, exist_ok=True)

                            last_download_path = remote_path_cache
                            local_logger.info(f"Downloading file from '{last_download_path}' to '{local_folder_path + remote_path_cache[1:]}'")
                            if sleep_time:
                                time.sleep(sleep_time)
                            try:
                                sftp.get(
                                    remote_path_cache, 
                                    local_folder_path + remote_path_cache[1:]
                                )
                            except PermissionError:
                                local_logger.error(f"Permission Denied '{last_download_path}'")
                                local_logger.warn(f"Trying to change permissions of file '{last_download_path}'")
                                if sleep_time:
                                    time.sleep(sleep_time)
                                status, output = ssh_execute_command(
                                    ssh_client=ssh_client,
                                    username=username,
                                    password=password,
                                    command=f"chmod 777 {last_download_path}",
                                    is_sudo=True,
                                    port=port,
                                    reboot=False
                                )
                                if status == False:
                                    local_logger.error(f"Error changing permissions of file '{last_download_path}'")
                                else:
                                    local_logger.info(f"Permissions changed to 777 of file '{last_download_path}'")
                                    local_logger.info(f"Re-Trying to Download file from '{last_download_path}' to '{local_folder_path + remote_path_cache[1:]}'")
                                    if sleep_time:
                                        time.sleep(sleep_time)
                                    sftp.get(
                                        remote_path_cache, 
                                        local_folder_path + remote_path_cache[1:]
                                    )
            else:
                local_logger.info(f"Downloading file from {remote_path} to {local_folder_path}...")
                last_download_path = remote_path
                if sleep_time:
                    time.sleep(sleep_time)
                sftp.get(last_download_path, local_folder_path)
        except FileNotFoundError:
            local_logger.error(f"[Errno 2] No such file: '{remote_path}'")
        finally:
            sftp.close()

        local_folder_path += os.path.basename(remote_path)
        response_download = True

    except paramiko.AuthenticationException:
        local_logger.error("Authentication failed")
        local_folder_path = ""
    except Exception as e:
        local_logger.error(f"Last Download Dir: {last_download_path}")
        local_logger.error(f"Exception: {e}")

        if response_download == False:
            local_folder_path = ""
        elif response_download == True:
            local_folder_path = local_folder_path
    finally:
        transport.close()

    return local_folder_path



def ssh_execute_command(ssh_client:str, username:str, password:str, command:str, port:int=22, timeout=5, is_sudo=False, reboot:bool=False, logger_hook=None) -> tuple[bool, str]:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    status = False
    client_stdout = ""
    
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
    
    
    try:
        client.connect(ssh_client, port, username, password, timeout=timeout)
        local_logger.info("Connection Established!")
        
        # update hostname
        # stdin, stdout, stderr = client.exec_command(f'echo {new_hostname} > /etc/hostname')
        if is_sudo:
            command = f'echo {password} | sudo -S {command}'
            # command = f'echo {password} | sudo -S sh -c "echo \'{command}\'"'
        
        local_logger.info(f"Executing command: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        client_stdout = stdout.read().decode()
        local_logger.info(f"stdout: {client_stdout}")
        
        exit_status = stdout.channel.recv_exit_status() # Blocking call
        if exit_status==0:
            local_logger.info("Command successfully executed!")
            status = True
            
            if reboot:
                stdin_reboot, stdout_reboot, stderr_reboot = client.exec_command('echo {password} | sudo -S reboot -h now')
            else:
                local_logger.info("Reboot skipped.")
        else:
            local_logger.error(f"STDOUT Detail: {stdout.read().decode()}")
            local_logger.error(f"STDERR Detail [Exit Status {exit_status}]: {stderr.read().decode()}")
            status = False
        
    except paramiko.AuthenticationException:
        local_logger.info("Authentication failed")
        status = False
    except Exception as e:
        local_logger.error(f"Exception: {e}")
        status = False
    finally:
        client.close()
        
    return status, client_stdout
    


def get_local_IP():
    return gethostbyname(gethostname())



def ping_by_ip(ip_address: str, legacy=False, port=22, logger_hook = None)-> bool:
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    if legacy:
        os_type = os.name

        if os_type == "nt":  # Windows
            ping_command = "ping -n 1 "
        else:  # Assume Linux or macOS
            ping_command = "ping -c 1 "

        command = ping_command + ip_address
        response = os.popen(command)

        local_logger.info("Response: ", response.readlines())

        for line in response.readlines():
            if "TTL" in line:
                # local_logger.info(ip_address, "--> Live")
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
    #         # logger.info(f'Port {port}: OPEN')
    #         is_open = True
    # finally:
    #     sock.close()
    
    is_open = False
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.settimeout(3)  # Set a timeout of 3 second
        try:
            conn = sock.connect_ex((ip_address, port))
            if conn == 0:
                # logger.info(f'Port {port}: OPEN')
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
    #     logger.info(f"IP: {scan_ip_address}, Hostname: {hostname}")
    # else:
    #     logger.info(f"IP: {scan_ip_address}")
        
    dict_ip_hostname_template = {
        "ip": "",
        "hostname": ""
    }

    entry = dict_ip_hostname_template.copy()
    entry["ip"] = scan_ip_address
    entry["hostname"] = hostname if hostname else ""
    return entry

    
    
def ping_sweeping_threaded(network_address:str, start:int=1, end:int=255, logger_hook=None)->list:
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    if network_address == "":
        network_address = get_local_IP()
        network_address = network_address[:network_address.rfind(".")] + ".x"
        local_logger.info(f"Selected Default IP Mask: {network_address}")
    
    network_address_splitted= network_address.split('.')
    last_dot = '.'

    network_address_clean = network_address_splitted[0] + last_dot + network_address_splitted[1] + last_dot + network_address_splitted[2] + last_dot

    list_ip_hostname = []

    local_logger.info("Starting to scan.")
    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        futures = []
        for i in range(start, end):
            scan_ip_address = network_address_clean + str(i)
            futures.append(executor.submit(scan_ip, scan_ip_address))

        local_logger.info("Scanning...")
        for future in concurrent.futures.as_completed(futures):
            entry = future.result()
            if entry is not None:
                list_ip_hostname.append(entry)
            
    # Sort the list by IP address
    list_ip_hostname = sorted(list_ip_hostname, key=lambda x: tuple(map(int, x['ip'].split('.'))))

    local_logger.info("Scanning completed.")
    
    return list_ip_hostname


    
def select_ip_addresses(ip_addresses:list, logger_hook=None)->list:
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    selected_ip_addresses = []
    
    local_logger.info("Select IP Addresses to connect over ssh:")
    print_ip_table(ip_hostname_pack=ip_addresses, logger_hook=logger_hook)

    selected_indexes = input("Please enter the IP Addresses to add to the Hosts File (separated by comma)[1,2,3]: ")
    selected_indexes = selected_indexes.split(",")
    selected_indexes = list(map(str.strip, selected_indexes))
    selected_indexes = [int(index) for index in selected_indexes if index != "" or index.isdigit()]

    for index in selected_indexes:
        selected_ip_addresses.append(ip_addresses[index])
    
    return selected_ip_addresses



def print_ip_table(ip_hostname_pack, logger_hook=None):
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
    # print(f"\tIP\t |\tHostname")
    
    local_logger.info(f"\tIP\t |\tHostname")
    for i, result in enumerate(ip_hostname_pack):
        local_logger.info(f" ({i})\t{result['ip']}\t |\t {result['hostname'] if result['hostname'] else '---'}")
        # print(f" ({i})\t{result['ip']}\t |\t {result['hostname'] if result['hostname'] else '---'}")
        


##################
### FQDN Tools ###
##################

def create_hosts_file(ip_address_hostnames_list: List[Dict[str, str]]=[], folder:str="/", logger_hook=None):
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
        
    local_logger.info("Creating hosts file...")
    print_ip_table(ip_address_hostnames_list, logger_hook=logger_hook)
    
    ip_address_to_host_list = list()
    ip_address_to_host_template = "{ip_address}\t{hostname}\n"

    hosts_file_template = """#Auto-generated hosts file with HPE Ezmeral Tools Platform by Treo Information Technologies for {ip_address}
    
127.0.0.1	localhost
127.0.0.1	{hostname}

{ip_address_to_host_string}

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
"""
    hosts_file_for_ip = {
        "ip_address": "",
        "hosts_file_content": ""
    }
    hosts_file_for_ip_list = list()
    
    
    for ip_address_hostname in ip_address_hostnames_list:
        
        temp_ip_address_host = ip_address_to_host_template.format(
            ip_address=ip_address_hostname["ip"],
            hostname=ip_address_hostname['hostname']
        )
        ip_address_to_host_list.append(temp_ip_address_host)
        
        
    for ip_address_hostname in ip_address_hostnames_list:
        ip_address_to_host_string = ''.join(
            string_item for string_item in ip_address_to_host_list
        )
        # ip_address_to_host_string = ""
        # for string_item in ip_address_to_host_list:
        #     if ip_address_hostname["ip"] in string_item:
        #         continue
        #     ip_address_to_host_string = ''.join(string_item)
        
        lines = ip_address_to_host_string.splitlines()
        lines = [line for line in lines if ip_address_hostname["ip"] not in line]
        ip_address_to_host_string = '\n'.join(lines)
        
        hosts_file_content = hosts_file_template.format(
            ip_address=ip_address_hostname["ip"],
            hostname=ip_address_hostname["hostname"],
            ip_address_to_host_string=ip_address_to_host_string
        )
        hosts_file_for_ip_list.append(
            hosts_file_for_ip.copy()
        )
        hosts_file_for_ip_list[-1]["ip_address"] = ip_address_hostname["ip"]
        hosts_file_for_ip_list[-1]["hosts_file_content"] = hosts_file_content
        
        local_logger.info(f"Hosts file content for {ip_address_hostname['ip']}: ")
        local_logger.info(hosts_file_content)
        
        folder = folder if folder[-1] == "/" else folder + "/"
        path = f"{folder}hosts_{ip_address_hostname['ip']}" # The path of your file should go here
        
        with open(path, "w") as file: # Opens the file using 'w' method. See below for list of methods.
            file.write(hosts_file_content) # Writes to the file used .write() method
            # file.close() # Closes file
            local_logger.info(f"Hosts file for {ip_address_hostname['ip']} created successfully.")
            
    return ip_address_hostnames_list


def send_hostfile_to_device_ssh(ssh_client:str, username:str, password:str, local_file_path:str, remote_file_path:str="/etc/", port:int=22, logger_hook=None):
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    
    try:
        transport = paramiko.Transport((ssh_client, port))
    except Exception as error:
        local_logger.error(f"Error creating Transport: {error}")
        return False

    try:
        transport.connect(username=username, password=password)
        sftp = transport.open_sftp_client()

        if sftp is None:
            local_logger.error("Error opening SFTP Client")
            return False

        # upload file to temporary location
        tmp_path = "/tmp/" + os.path.basename(local_file_path)
        sftp.put(local_file_path, tmp_path)
        sftp.close()

        # move file to final location with sudo
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ssh_client, port, username, password)
        stdin, stdout, stderr = client.exec_command(f'echo {password} | sudo -S mv {tmp_path} {remote_file_path}')
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            local_logger.info(f"File {local_file_path} successfully sent to {remote_file_path}")
        else:
            local_logger.error(f"Error moving file to final location, status code {exit_status}")
            local_logger.error(f"Detail: {stderr.read().decode()}")

    except paramiko.AuthenticationException:
        local_logger.error("Authentication failed")
        return False
    except Exception as error:
        local_logger.error(f"Exception: {error}")
        return False
    finally:
        transport.close()

    return True
    
        
def update_hostname_ssh(ssh_client:str, username:str, password:str, new_hostname:str, port:int=22, reboot:str="y", logger_hook=None) -> int: 
    
    if logger_hook is not None:
        local_logger = logger_hook
    else:
        local_logger = logger
        
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ssh_client, port, username, password)
        
        # update hostname
        # stdin, stdout, stderr = client.exec_command(f'echo {new_hostname} > /etc/hostname')
        stdin, stdout, stderr = client.exec_command(f'echo {password} | sudo -S sh -c "echo \'{new_hostname}\' > /etc/hostname"')
        exit_status = stdout.channel.recv_exit_status() # Blocking call
        if exit_status==0:
            local_logger.info("Hostname updated successfully")
    
            # Hosts dosyasını güncelle
            stdin, stdout, stderr = client.exec_command('sudo sed -i -e "s/^127\.0\.1\.1.*/127.0.1.1\t{}/" /etc/hosts'.format(new_hostname))
            stdin.write(f'{password}\n')  # Sudo parolasını buraya yazın
            stdin.flush()
    
            if reboot == "y":
                stdin, stdout, stderr = client.exec_command('sudo reboot -h now')
            else:
                local_logger.info("Reboot skipped.")
        else:
            local_logger.error("Error", exit_status)
            local_logger.error("Detail:", stderr.read().decode())
            return exit_status
        
    except paramiko.AuthenticationException:
        local_logger.error("Authentication failed")
        return -1
    except Exception as error:
        local_logger.error(f"Exception: {error}")
        return -1
    finally:
        client.close()
        
    return 0