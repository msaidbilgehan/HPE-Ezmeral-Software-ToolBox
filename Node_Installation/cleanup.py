import os



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



def cleanup():
    commands = [
        "sudo apt --fix-broken install",
        "sudo docker stop $(sudo docker ps -a -q)",
        "sudo docker rmi $(sudo docker images -a -q) -f",
        "sudo systemctl stop docker",
        "sudo apt-get remove -y docker docker-engine docker.io containerd runc",
        "sudo apt-get purge -y docker docker-engine docker.io containerd runc",
        "sudo apt-get autoremove -y --purge docker docker-engine docker.io containerd runc",
        "sudo apt-get --purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
        # "sudo apt-get purge -y docker-ce docker-ce-cli",
        "sudo rm -rf /var/lib/docker /etc/docker",
        "sudo rm /lib/systemd/system/docker.service"
        "sudo rm /etc/apparmor.d/docker",
        "sudo groupdel docker",
        "sudo rm -rf /var/run/docker.sock /var/lib/docker.sock ~/.docker /usr/local/bin/docker-compose",
        "sudo systemctl daemon-reload",
        "sudo systemctl reset-failed",
        "sudo apt-get remove --purge -y mapr-*",
        "sudo rm -r /opt/mapr/zookeeper",
        "sudo apt --fix-broken install",
        "sudo apt autoremove -y",
        "sudo dpkg --configure -a",
    ]
    for command in commands:
        os.system(command)


if __name__ == "__main__":
    initialize_message()
    cleanup()
    print("Highly Recommended to restart the system. (sudo reboot -h now)")
    print("Exiting...")
    exit()