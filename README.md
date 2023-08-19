
# Ubuntu 18.04-20.04 Installation on HPE Datafabric

## Minimum Requirements

### Storage

- /: 50 Gb - 275 Gb
- /var: 150 Gb - 175 Gb
- /srv: 100 Gb - 150 Gb
- /opt: 128 Gb - 150 Gb
- swap: 30 Gb
- No-Formatted: 100 Gb - 120 Gb

### Resource Requirements

- Memory: 65 Gb - 100 Gb
- CPU: 16 Core

## Technical Requirements

### User Passwordless Sudo

```bash
sudo nano /etc/sudoers
mapr
ALL=(ALL:ALL) NOPASSWD:ALL
```

### Local Configuration

```bash
sudo nano /etc/apt/sources.list
```

### Install Software from Repo

```bash
sudo apt install openssh-server neofetch htop net-tools -y
```

### [Disable Auto Updates](https://linuxhint.com/disable-automatic-updates-ubuntu/)

```bash
sudo nano /etc/apt/apt.conf.d/20auto-upgrades
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
APT::Periodic::Unattended-Upgrade "1";
```

### [Swap Priority Change](https://askubuntu.com/questions/778683/swap-priority-gets-set-to-1-on-each-boot)

```bash
sudo swapoff -a
sudo nano /etc/fstab
```

### [Swappiness Change](https://askubuntu.com/questions/103915/how-do-i-configure-swappiness)

```bash
sudo nano /etc/sysctl.conf
vm.swappiness = 55
sudo sysctl --load
```

### Add Neofetch and IP Command

```bash
sudo nano ~/.bashrc
neofetch
ifconfig | grep "inet 10.34.2.*\n"
```

### [Install Docker](https://docs.docker.com/engine/install/ubuntu/)

### Set Root Password and [SSH Configuration](https://askubuntu.com/questions/497895/permission-denied-for-rootlocalhost-for-ssh-connection)

```bash
sudo passwd root
sudo nano /etc/ssh/sshd_config
PermitRootLogin yes
PasswordAuthentication yes
ChallengeResponseAuthentication no
sudo systemctl restart sshd
ssh root@localhost
```

### [Change UID and GID of User to 5000](https://www.cyberciti.biz/faq/linux-change-user-group-uid-gid-for-all-owned-files/#:~:text=Linux%20command%20to%20change%20UID%20and%20GID)

```bash
ssh root@localhost
usermod -u 5000 mapr
groupmod -g 5000 mapr
```

### [Or Add New User with Specific UID-GID](https://docs.ezmeral.hpe.com/datafabric-customer-managed/73/AdvancedInstallation/c_install_prerequisites.html#:~:text=Chrome-,Cluster%20Admin%20User%20Requirements,-The%20installation%20process)

```bash
useradd -m -u $MAPR_UID -g $MAPR_GID -G $(stat -c '%G' /etc/shadow) $MAPR_USER
MAPR_USER defaults to mapr.
MAPR_UID defaults to 5000.
MAPR_GID defaults to 5000.
```

### [Install Cloud-Init](https://www.ibm.com/docs/pt/powervc/1.4.4?topic=linux-installing-configuring-cloud-init-ubuntu)

### Mapr-Setup Installation Steps

## Mapr-Setup Installation Steps

1. `sudo chmod u+s /sbin/unix_chkpwd`
2. `sudo apt install openjdk-11-jre openjdk-11-jre-headless`
3. Download the Mapr-Setup script:

    ```bash
    wget --user=<user> --password=<password> https://package.ezmeral.hpe.com/releases/installer/mapr-setup.sh
    chmod +x mapr-setup.sh
    ```

      1. Don’t forget to delete the “-T” value for the wget command in the `mapr-setup.sh` script.
      2. Execute the setup:

            ```bash
            sudo ./mapr-setup.sh -r https://<user>:<password>@package.ezmeral.hpe.com/releases/
            ```

4. For every Node, you need to add the public key of the apt repository:

   ```bash
   wget --user <user> --password <password> https://package.ezmeral.hpe.com/releases/installer/ubuntu/pub/maprgpg.key
   sudo apt-key add maprgpg.key
   ```

   1. Access the installer at `https://<Installer Node hostname/IPaddress>:9443`.

5. More details of the mapr-setup script can be found [here](https://docs.ezmeral.hpe.com/datafabric-customer-managed/73/AdvancedInstallation/c_installer_how_it_works.html).
6. For License search Data Fabric Community Edition, visit [this link](https://myenterpriselicense.hpe.com/cwp-ui/software).
7. For the Installer Troubleshooting, refer to [this guide](https://docs.ezmeral.hpe.com/datafabric-customer-managed/73/AdvancedInstallation/troubleshooting_mapr_installer.html).
