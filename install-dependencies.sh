#!/usr/bin/env bash

function aptInstall() {
	binary=("$@")
	for i in "${binary[@]}" ; do
		dpkg -s "$i" &> /dev/null
		if [ "$?" -ne 0 ] 
		then

			echo ""$i" not installed"
			sudo apt-get install -y "$i"
		else
			echo ""$i" is already installed"
		fi
	done
}



# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


wget -O - https://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
add-apt-repository \
	"deb [arch=amd64] http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest \
    $(lsb_release -cs) \
    main"

#echo "deb http://repo.saltstack.com/apt/ubuntu/18.04/amd64/latest bionic main" >> /etc/apt/sources.list.d/saltstack.list



dock_comp_v="docker-compose --version"
dock_comp="docker-compose"


declare -a primary_binary=("docker-ce" "docker-ce-cli" "containerd.io" "python3" "tcl" "python3-pip" "git" )

sudo apt-get update

aptInstall "${primary_binary[$@]}"


$dock_comp_v &> /dev/null
if [ "$?" -ne 0 ] 
then
	# Download the current stable release of Docker Compose
	curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	# Apply executable permissions to the Docker Compose binary:
	chmod +x /usr/local/bin/docker-compose

	# Creating a symbolic link to /usr/bin/docker-compose
	ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

	# Download and install bash command completion for Docker Compose
	curl -L https://raw.githubusercontent.com/docker/compose/1.25.4/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose

	# Post Installation set up for Docker
	# Manage Docker as a non root user
	# Create the docker group
	sudo groupadd docker
	# Add vagrant user to the docker group
	sudo usermod -aG docker $(whoami)

else
	echo ""$dock_comp" is already installed"
fi

vbox_v="vboxmanage -v"
vbox="virtualbox"

vagran_v="vagrant --version"
vagrant="vagrant"

echo "Downloading and installing Virtualbox"
curl -o $vbox.deb https://download.virtualbox.org/virtualbox/6.1.4/virtualbox-6.1_6.1.4-136177~Ubuntu~eoan_amd64.deb
apt install -y ./$vbox.deb
rm -f ./$vbox.deb

echo "Downloading and installing Vagrant"
curl -o $vagrant.deb https://releases.hashicorp.com/vagrant/2.2.7/vagrant_2.2.7_x86_64.deb
apt install -y ./$vagrant.deb
rm -f ./$vagrant.deb


# Installing Saltstack on Hostmachine


systemctl start docker.service