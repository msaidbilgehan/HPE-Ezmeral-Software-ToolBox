import os
from docker_setup import docker_setup


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


def run_setup_script():
    os.system("python3 ./setup_dependencies.py")



if __name__ == "__main__":
    initialize_message()
    docker_setup()
    run_setup_script()
    print("Exiting...")
    exit()