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
    print('Setting up dependencies...')
    print('Loading deb packages from dependencies folder...')



def prepare():
    commands = [
        "sudo apt update",
        # "sudo apt-get remove -y docker docker-engine docker.io containerd runc",
        "sudo apt-get -y install ca-certificates curl gnupg",
        "sudo install -m 0755 -d /etc/apt/keyrings",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        "sudo chmod a+r /etc/apt/keyrings/docker.gpg",
        "echo \
            \"deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
            \"$(. /etc/os-release && echo \"$VERSION_CODENAME\")\" stable\" | \
            sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \
        ",
        "sudo apt update",
        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
        # "sudo apt install docker.io -y",
        "sudo systemctl start docker",
        "sudo systemctl enable docker",
        "sudo docker --version",
    ]
    for command in commands:
        os.system(command)


def run_setup_script():
    os.system("python3 ./setup_dependencies.py")



if __name__ == "__main__":
    initialize_message()
    prepare()
    run_setup_script()
    print("Exiting...")
    exit()