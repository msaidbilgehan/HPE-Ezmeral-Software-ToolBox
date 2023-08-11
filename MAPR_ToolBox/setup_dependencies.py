from glob import glob
import os
import platform
import shutil, stat
import urllib.request
import subprocess



dependency_path=os.path.abspath("./dependencies/")

# Java Home Path
java_home_command = "readlink -f $(which java) | sed 's:/bin/java::'"



def initialize_message():
    print('-----------------------------------')
    print('TREO Information Technologies')
    print('https://www.treo.com.tr/')
    print('-----------------------------------')
    print('Node Installation Script')
    print('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    print('All Rights reserved.')
    print('Version 1.0')
    print('-----------------------------------')
    print('Setting up dependencies...')
    print('Loading deb packages from dependencies folder...')



def health_check_dependency_packages():
    necessary_scripts = ["mapr_devsandbox_container_setup.sh"]
    necessary_packages = [
        "mapr-client-7.2", 
        "mapr-hadoop-util_3.3.4", 
        "mapr-librdkafka_0.11.3", 
        "mapr-core-internal-7.2", 
        "mapr-core_7.2", 
        "mapr-zk-internal_7.2", 
        "mapr-zookeeper_7.2",
        "mapr-fileserver_7.2", 
        "mapr-cldb_7.2", 
        "mapr-nfs_7.2", 
        "mapr-nfs4server_7.2", 
        "mapr-nfsganesha_3.3", 
    ]
    missing_files = []

    deb_files = glob(dependency_path + '/*.deb')
    
    if len(deb_files) == 0:
        print("No deb files found in the dependencies folder.")
        print("Please download the necessary deb files and put them in the dependencies folder.")
        print("Exiting...")
        exit()
        
    script_files = glob(dependency_path + '/*.sh')
    if len(script_files) == 0:
        print("No script files found in the dependencies folder.")
        print("Please download the necessary script files and put them in the dependencies folder.")
        print("Exiting...")
        exit()
    
    ordered_deb_files = list()
    for package in necessary_packages:
        is_missing = True
        for deb_file in deb_files:
            if package in deb_file:
                is_missing = False
                ordered_deb_files.append(deb_file)
                break
        if is_missing:
            missing_files.append(package)
            
    for script in necessary_scripts:
        is_missing = True
        for script_file in script_files:
            if script in script_file:
                is_missing = False
                break
        if is_missing:
            missing_files.append(script)
            
    if len(missing_files) > 0:
        print("Missing files:")
        for file in missing_files:
            print("  -", file)
        print("Please download the missing files and put them in the dependencies folder.")
        print("Exiting...")
        exit()
    else:
        print("[PASSED] All necessary files are present in the dependencies folder.")
        
    ordered_deb_files = sorted(deb_files, key=lambda f: int(f.split('/')[-1].split('_')[0].split('_')[-1]))
    return ordered_deb_files, script_files


def health_check_os():
    print("Checking OS...")
    os_name = platform.system().lower()
    if os_name == "posix" or os_name == "linux":
        print("[PASSED] OS is Linux.")
        
        linux_distribution = platform.platform().lower()
        if "ubuntu" in linux_distribution and "18.04" in linux_distribution and ("x64bit" in linux_distribution or "x86_64" in linux_distribution):
            print("[PASSED] OS is Ubuntu 18.04 x64bit")
            return True
        else:
            print(f"{linux_distribution} is not supported.")
            print("Exiting...")
            exit()
    else:
        print(f"{os_name} OS is not yet supported.")
        print("Exiting...")
        exit()
    


def install_pre_dependency_packages(apt_apps):
    print("Installing dependency from apt...")
    os.system(f"sudo apt update")
    for app in apt_apps:
        os.system(f"sudo apt install -y {app}")
        
    print("Dependency packages installed from apt successfully.")
    return True



def download_dependency_packages():
    print(f"Downloading dependency packages to {dependency_path} ...")
    download_links = [
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-cldb_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-client-7.2.0.0.20230118195227.GA-1.amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-core-internal-7.2.0.0.20230118195227.GA-1.x86_64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-core_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-fileserver_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-nfs4server_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-nfs_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-nfsganesha_3.3.0.0.202111090944_all.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-zk-internal_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/v7.2.0/ubuntu/mapr-zookeeper_7.2.0.0.20230118195227.GA-1_amd64.deb",
        "https://package.mapr.hpe.com/releases/MEP/MEP-9.1.1/ubuntu/mapr-librdkafka_0.11.3.202201311452_amd64.deb",
        "https://package.mapr.hpe.com/releases/MEP/MEP-9.1.1/ubuntu/mapr-hadoop-util_3.3.4.200.202304060556_amd64.deb",
        "https://raw.githubusercontent.com/mapr-demos/mapr-db-720-getting-started/main/mapr_devsandbox_container_setup.sh",
    ]
    if os.path.exists(dependency_path):
        shutil.rmtree(dependency_path)
    os.mkdir(dependency_path)
    os.chmod(dependency_path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
    
    for i, file_url in enumerate(download_links):
        print(f"Downloading {file_url} ...")
        urllib.request.urlretrieve(file_url, dependency_path + "/" + str(i) + "_" + file_url.split("/")[-1])

    print("Dependency packages downloaded successfully.")
    return True



def install_dependency_packages(deb_files):
    print("Installing dependency packages...")
    for package in deb_files:
        os.system(f"sudo dpkg -i {package}")
        
    os.system(f"sudo apt --fix-broken install -y")
    
    print("Dependency packages installed successfully.")
    return True



def install_mapr_container(scripts):
    print("Installing mapr container...")
    for script in scripts:
        os.system(f"sudo chmod +x {script}")
        os.system(f"sudo {script}")
    print("Mapr container installed successfully.")
    return True



if __name__ == "__main__":
    initialize_message()
    health_check_os()
    download_dependency_packages()
    deb_files, script_files = health_check_dependency_packages()
    install_pre_dependency_packages(["sdparm", "openjdk-11-jdk", "openjdk-11-jdk-headless", "nfs-common", "keyutils", "libjemalloc-dev", "libjemalloc1", "libnfsidmap2", "libtirpc1", "liburcu-dev", "liburcu6", "rpcbind"])
    install_dependency_packages(deb_files)
    install_mapr_container(script_files)
    
    print("Exiting...")
    exit()