#!/bin/bash

#####################################################
# Provision myvnp instance with SSM (& other deps)  
#####################################################

# Logs send to:
LOGS="/var/log/myvpn.log"

function LOG (
    TXT=${1} 
    echo "$(date '+%Y-%m-%d %H:%M:%S %:z') [i] ${TXT}" >> ${LOGS}
)

LOG "Bootstraping myvpn..."

# Make log file
if [ ! -f ${LOGS} ] 
then
    touch ${LOGS}
fi

# Install SSM
if [ $(systemctl is-active amazon-ssm-agent) == 'active' ]
then
    LOG "SSM is already $(systemctl is-active amazon-ssm-agent)"
else
    LOG "SSM is $(systemctl is-active amazon-ssm-agent), setting up..."
    mkdir /tmp/ssm
    cd /tmp/ssm
    wget -q https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/debian_amd64/amazon-ssm-agent.deb
    LOG "Installing SSM .deb..."
    dpkg -i amazon-ssm-agent.deb
    LOG "SSM is now $(systemctl is-active amazon-ssm-agent)"
fi

# Install Ansible
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install python3-pip
python3 -m pip install --user ansible
export PATH=$PATH:~/.local/bin

# Permit @root login - primarily for ansible
sed -i 's/^.*ssh-rsa/ssh-rsa/' /root/.ssh/authorized_keys
sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin without-password/' /etc/ssh/sshd_config
sysctl restart ssh.service