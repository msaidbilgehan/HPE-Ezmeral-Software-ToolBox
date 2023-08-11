import os
import sys



def initialize_message():
    print('-----------------------------------')
    print('TREO Information Technologies')
    print('https://www.treo.com.tr/')
    print('-----------------------------------')
    print('MAPR Cleanup Script')
    print('Created By Muhammed Said BİLGEHAN and Mirza ÖZER')
    print('All Rights reserved.')
    print('Version 1.0')
    print('-----------------------------------')



def cleanup():
    commands = [
        "{} apt --fix-broken install",
        "{} docker stop $(sudo docker ps -a -q)",
        # "{} docker rmi $(sudo docker images -a -q) -f",
        "{} systemctl stop docker",
        "{} apt-get remove -y docker docker-engine docker.io containerd runc",
        "{} apt-get purge -y docker docker-engine docker.io containerd runc",
        "{} apt-get autoremove -y --purge docker docker-engine docker.io containerd runc",
        "{} apt-get remove --purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
        "{} rm -rf /var/lib/docker /etc/docker",
        "{} rm /lib/systemd/system/docker.service",
        "{} rm /etc/apparmor.d/docker",
        "{} groupdel docker",
        "{} rm -rf /var/run/docker /var/lib/docker /var/run/docker.sock /var/lib/docker.sock ~/.docker /usr/local/bin/docker-compose",
        "{} systemctl daemon-reload",
        "{} systemctl reset-failed",
        "{} apt-get remove --purge -y mapr-*",
        "{} rm -rf /opt/mapr",
        "{} apt --fix-broken install",
        "{} apt autoremove -y",
        "{} dpkg --configure -a",
        "echo Rebooting in 3 seconds...",
        "sleep 1",
        "echo .",
        "sleep 1",
        "echo .",
        "sleep 1",
        "echo .",
        "{} reboot -h now",
    ]
    for command in commands:
        if len(sys.argv) == 2:
            print(f"Running: echo {sys.argv[1]} | {command.format('sudo -S')}")
            os.system(f"echo {sys.argv[1]} | {command.format('sudo -S')}")
        else:
            print("Running:", command.format("sudo"))
            os.system(command.format("sudo"))


if __name__ == "__main__":
    initialize_message()
    print("Be aware! This script will delete all docker and mapr packages, and reboot your system.")
    cleanup()
    print("Exiting...")
    exit()