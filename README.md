# Document Streaming for JSON files
Note: This setup is for **Windows Subsystems for Linux (WSL)**.

To install WSL just open and run the Command Prompt as administrator and type the following command:

```bash
wsl --install
```

## Install Docker and Docker Compose with WSL2
Follow this [link](https://nickjanetakis.com/blog/install-docker-in-wsl-2-without-docker-desktop) to install Docker and Docker Compose in WSL2

```bash
# Uninstall older versions of Docker and Docker compose
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker, you can ignore the warning from Docker about using WSL
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the Docker group
sudo usermod -aG docker $USER

# Install Docker Compose v2
sudo apt-get update && sudo apt-get install docker-compose-plugin

# Sanity check that both tools were installed successfully
docker --version
docker compose version

# Using Ubuntu 22.04 or Debian 10 / 11? You need to do 1 extra step for iptables
# compatibility, you'll want to choose option (1) from the prompt to use iptables-legacy.
sudo update-alternatives --config iptables

# Start Docker service
service docker start

# Check if docker was installed properly
docker run hello-world
```

**Docker Service Start, Stop, Status, Restart commands**
```bash
# Start docker service
service docker start

# Docker service status
service docker status

# Docker service stop
service docker stop

# Restart docker service
service docker restart
```

## References 
  - https://github.com/zekeriyyaa/Apache-Spark-Structured-Streaming-Via-Docker-Compose
  - Data Making Youtube Channel