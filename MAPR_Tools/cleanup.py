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
        "for servis in $(systemctl list-units --type=service --no-legend | grep mapr- | awk '{{print $1}}'); do {} systemctl stop $servis && systemctl disable $servis; done",
        "for paket in $(dpkg -l | grep mapr- | awk '{{print $2}}'); do {} apt-get remove --purge -y $paket; done",
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
        "{} apt --fix-broken install",
        "{} apt autoremove -y",
        "{} dpkg --configure -a",
        "{} rm -rf /opt/mapr",
        "echo Rebooting in 3 seconds...",
        "sleep 1",
        "echo .",
        "sleep 1",
        "echo .",
        "sleep 1",
        "echo .",
        "{} reboot -h now",
    ]
    print("Running Commands Below;")
    for command in commands:
        if len(sys.argv) == 2:
            print(f"\t{command.format(f'echo {sys.argv[1]} | sudo -S')}")
            os.system(command.format(f'echo {sys.argv[1]} | sudo -S'))
        else:
            print(f"\t{command.format('sudo')}")
            os.system(command.format("sudo"))


if __name__ == "__main__":
    initialize_message()
    print("Be aware! This script will delete all docker and mapr packages, and reboot your system.")
    cleanup()
    print("Exiting...")
    exit()