# Installation (docker environment)

1. Remove default docker packages(old versions)
    ```bash
    sudo apt-get purge docker \
                       docker-engine \
                       docker.io \
                       lxc-docker 
    ```

2. Install required packages for installing docker
    ```bash
    sudo apt-get install curl \
                         apt-transport-https \
                         ca-certificates \
                         software-properties-common
    ```

3. Import docker GPG key to verified packages signiture
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    ```

4. Add docker repository
    ```bash
    sudo add-apt-repository \
         "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
         $(lsb_release -cs) stable"
    sudo apt-get update
    ```

5. Install docker(docker-ce) and docker-compose
    ```bash
    sudo apt-get install docker-ce \
                         docker-ce-cli \
                         containerd.io \
                         docker-compose
    ```
    
    Give user a root permission
    ```bash
    sudo usermod -aG docker $USER
    ```

6. Install nvidia-docker2
    Remove nvidia-docker1.0
    ```bash
    docker volume ls -q -f driver=nvidia-docker | \
    xargs -r -I{} -n1 docker ps -q -a -f volume={} | \
    xargs -r docker rm -f
    sudo apt-get purge nvidia-docker
    ```
    
    Add nvidia-docker repository
    ```bash
    curl -sL https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    dist=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -sL https://nvidia.github.io/nvidia-docker/$dist/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update
    ```
    
    Install nvidia-docker2
    ```bash
    sudo apt-get install nvidia-docker2
    sudo pkill -SIGHUP dockerd
    ```
    
    Set nvidia-docker as default-runtime of docker
    ```bash
    sudo vi /etc/docker/daemon.json
    ```
    ```json
    {
        "default-runtime": "nvidia",
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        }
    }
    ```
    ```bash
    sudo systemctl restart docker
    ```
    
    ```bash
    sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
    sudo chmod g+rwx "/home/$USER/.docker" -R
    ```
    
    Re-login is required

    Test nvidia-docker
    ```bash
    docker run --rm -it nvidia/cuda nvidia-smi
    ```
	