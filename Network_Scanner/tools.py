

import os
from socket import socket, AF_INET, SOCK_STREAM, gethostbyaddr, gethostbyname
import concurrent.futures
import subprocess
from dns import reversename, resolver
import paramiko


def print_ip_table(ip_hostname_dict):
    print(f"\tIP\t |\tHostname")
    for i, result in enumerate(ip_hostname_dict):
        print(f" ({i})\t{result['ip']}\t |\t {result['hostname'] if result['hostname'] else '---'}")


def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


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


def ___get_hostname_by_ip(ip_address:str):
    reversed_dns = reversename.from_address(ip_address)
    try:
        return str(resolver.resolve(reversed_dns,"PTR")[0])
    except resolver.NXDOMAIN:
        return ""


def __get_hostname_by_ip(ip_address:str):
    command = "host " + ip_address
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error is not None:
        return None
    return str(output).split(' ')[-1]


def get_hostname_by_ip(ip_address:str):
    try:
        return gethostbyaddr(ip_address)[0]
    except:
        return None
    
    
def get_ip_by_hostname(hostname:str):
    try:
        return gethostbyname(hostname)
    except:
        return None


def __port_scanner(ip_address:str):
    if ip_address == "":
        print("Please enter an IP address.")
        return
    
    for i in range(0, 50000):
      s = socket(AF_INET, SOCK_STREAM)
      
      conn = s.connect_ex((ip_address, i))
      if(conn == 0) :
         print ('Port %d: OPEN' % (i,))
      s.close()
      

# define the function to scan a single port
def scan_port(ip_address:str, port:int):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(3)  # Set a timeout of 3 second
    is_open = False
    try:
        conn = s.connect_ex((ip_address, port))
        if conn == 0:
            # print(f'Port {port}: OPEN')
            is_open = True
    finally:
        s.close()
    
    return port, is_open


def port_scanner(ip_address:str, start_range=0, end_range=50000):
    if ip_address == "":
        print("Please enter an IP address.")
        return
    
    # Ping the target IP
    if not ping_by_ip(ip_address):
        print("The IP is not reachable")
        return
    else:
        print("The IP is reachable. Starting to scan ports...")
    
    port_scan_tasks = []
    open_port_list = []
    # Create a ThreadPool, adjust the max_workers parameter to the number of cores you want to use
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        # Use the executor to start a task for each port
        for i in range(start_range, end_range):
            executor.submit(scan_port, ip_address, i)
            port_scan_tasks.append(executor.submit(scan_port, ip_address, i))

        print("Scanning...")

        for port_scan_task in concurrent.futures.as_completed(port_scan_tasks):
            port, is_open = port_scan_task.result()
            if is_open:
                open_port_list.append(port)
        
    print("")
    print(f"Open Ports: {open_port_list}")
    
      
def ping_sweeping(network_address:str, start:int=1, end:int=255):
    if network_address == "":
        print("Please enter an Network Address.")
        return
    
    network_address_splitted= network_address.split('.')
    last_dot = '.'

    network_address_clean = network_address_splitted[0] + last_dot + network_address_splitted[1] + last_dot + network_address_splitted[2] + last_dot

    dict_ip_hostname_template = {
        "ip": "",
        "hostname": ""
    }
    list_ip_hostname = []
    
    for i in range(start, end):
        scan_ip_address = network_address_clean + str(i)
        response = ping_by_ip(scan_ip_address)
        
        if response == False:
            continue
        
        hostname = get_hostname_by_ip(scan_ip_address)
        
        # if hostname:
        #     print(f"IP: {scan_ip_address}, Hostname: {hostname}")
        # else:
        #     print(f"IP: {scan_ip_address}")
            
        list_ip_hostname.append(
            dict_ip_hostname_template.copy()
        )
        list_ip_hostname[-1]["ip"] = scan_ip_address
        list_ip_hostname[-1]["hostname"] = hostname
    
    # Sort the list by IP address
    list_ip_hostname = sorted(list_ip_hostname, key=lambda x: tuple(map(int, x['ip'].split('.'))))
    
    return list_ip_hostname


def ping_sweeping_threaded(network_address:str, start:int=1, end:int=255)->list:
    if network_address == "":
        print("Please enter an Network Address.")
        return []
    
    network_address_splitted= network_address.split('.')
    last_dot = '.'

    network_address_clean = network_address_splitted[0] + last_dot + network_address_splitted[1] + last_dot + network_address_splitted[2] + last_dot

    list_ip_hostname = []

    print(f"Starting to scan.")
    with concurrent.futures.ThreadPoolExecutor(255) as executor:
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


def save_to_json(data, path:str="results.json"):
    import json
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
        
        
def load_from_json(path:str="results.json"):
    import json
    with open(path) as json_file:
        data = json.load(json_file)
        return data
        
        
def create_hosts_file(ip_address_hostname_list=[], filename:str="hosts"):
    print("Creating hosts file...")
    print_ip_table(ip_address_hostname_list)
    
    ip_address_to_host_list = list()
    ip_address_to_host_template = "{ip_address}\t{hostname}\n"

    hosts_file_template = """#Auto-generated hosts file with Network Scanner by Muhammed Said BİLGEHAN for {ip_address}
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
    
    
    for ip_address_hostname in ip_address_hostname_list:
        ip_address_hostname['hostname']=input(f"Please enter a hostname for {ip_address_hostname['ip']}: ")
        
        temp_ip_address_host = ip_address_to_host_template.format(
            ip_address=ip_address_hostname["ip"],
            hostname=ip_address_hostname['hostname']
        )
        ip_address_to_host_list.append(temp_ip_address_host)
        
        
    for ip_address_hostname in ip_address_hostname_list:
        ip_address_to_host_string = ''.join(
            string_item for string_item in ip_address_to_host_list if ip_address_hostname["ip"] =! string_item
        )
        
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
        
        print(f"Hosts file content for {ip_address_hostname['ip']}: ")
        print(hosts_file_content)
        
        path = f"hosts_{ip_address_hostname['ip']}" # The path of your file should go here
        with open(path, "w") as fil: # Opens the file using 'w' method. See below for list of methods.
            fil.write(hosts_file_content) # Writes to the file used .write() method
            # fil.close() # Closes file
            print(f"Hosts file for {ip_address_hostname['ip']} created successfully.")
            
    return ip_address_hostname_list

def send_hostfile_to_device_ssh(ip_address:str, username:str, password:str, local_file_path:str, remote_file_path:str="/etc/", port:int=22):
    transport = paramiko.Transport((ip_address, port))
    
    try:
        transport.connect(username=username, password=password)
        sftp = transport.open_sftp_client()

        if sftp is None:
            print("Error opening SFTP Client")
            return False

        # upload file to temporary location
        tmp_path = "/tmp/" + os.path.basename(local_file_path)
        sftp.put(local_file_path, tmp_path)
        sftp.close()

        # move file to final location with sudo
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip_address, port, username, password)
        stdin, stdout, stderr = client.exec_command(f'echo {password} | sudo -S mv {tmp_path} {remote_file_path}')
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(f"File {local_file_path} successfully sent to {remote_file_path}")
        else:
            print(f"Error moving file to final location, status code {exit_status}")
            print(f"Detail: {stderr.read().decode()}")

    except paramiko.AuthenticationException:
        print("Authentication failed")
    finally:
        transport.close()

    return True
    
        
def update_hostname_ssh(ip_address:str, username:str, password:str, new_hostname:str, port:int=22, reboot:str="y"):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ip_address, port, username, password)
        
        # update hostname
        # stdin, stdout, stderr = client.exec_command(f'echo {new_hostname} > /etc/hostname')
        stdin, stdout, stderr = client.exec_command(f'echo {password} | sudo -S sh -c "echo \'{new_hostname}\' > /etc/hostname"')
        exit_status = stdout.channel.recv_exit_status() # Blocking call
        if exit_status==0:
            print("Hostname updated successfully")
    
            # Hosts dosyasını güncelle
            stdin, stdout, stderr = client.exec_command('sudo sed -i -e "s/^127\.0\.1\.1.*/127.0.1.1\t{}/" /etc/hosts'.format(new_hostname))
            stdin.write(f'{password}\n')  # Sudo parolasını buraya yazın
            stdin.flush()
    
            if reboot == "y":
                stdin, stdout, stderr = client.exec_command('sudo reboot -h now')
            else:
                print("Reboot skipped.")
        else:
            print("Error", exit_status)
            print("Detail:", stderr.read().decode())
        
    except paramiko.AuthenticationException:
        print("Authentication failed")
    finally:
        client.close()
        
