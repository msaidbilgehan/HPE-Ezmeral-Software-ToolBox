import os



def docker_setup():
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



if __name__ == "__main__":
    print("Docker installation is starting...")
    docker_setup()
    print("Exiting...")
    exit()