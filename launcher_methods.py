import os
import boto3
import subprocess
from typing import Optional
from botocore.config import Config

"""
   Methods file to deploy & configure vpn on aws
"""

# TODO: mk this part of user config etc.
MYVPN_CONFG = Config(
    region_name = 'eu-west-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)


# TODO: properly manage cloud providers
def get_cloud_provider():
    return "AWS"

# TODO: manage ansible ssh users properly
def ansible_ssh_user() -> str:
    if get_cloud_provider() == "AWS":
        return "admin"
    
    raise NotImplementedError()


# Plan myvpn from terrafrom
def plan_vpn():
    print("[i] Planning instance from tf configuration...")
    subprocess.run("terraform plan -var-file=my.tfvars", shell=True, check=True)
    return True


# Deploy myvpn with terrafrom apply
def deploy_vpn():
    print("[i] Creating instance from tf configuration...")
    subprocess.run("terraform apply -var-file=my.tfvars", shell=True, check=True)
    return True


# Destroy myvpn from terrafrom destroy
def destroy_vpn():
    print("[i] Destroying instance from tf configuration...")
    subprocess.run("terraform destroy -var-file=my.tfvars", shell=True, check=True)
    return True


# Destroy & re-create myvpn from terrafrom
def redeploy_vpn():
    print("[i] Redploying your vpn instance...")
    subprocess.run("terraform destroy -target=aws_instance.webserver -var-file=my.tfvars", shell=True, check=True)
    subprocess.run("terraform apply -var-file=my.tfvars", shell=True, check=True)


# Determine whether or myvpn is runnig
def isrunning(ec2) -> bool:
    response = ec2.describe_instances(Filters=[ {'Name': 'instance-state-name', 'Values': ['running']} ] )
    if len(response['Reservations']):
        return True
    return False


# Get myvnp address resp
def getvpn_address() -> str:
    ec2 = boto3.client('ec2', region_name="eu-west-1")
    if isrunning(ec2):
        filters = [ {'Name': 'domain', 'Values': ['vpc']} ]
        response = ec2.describe_addresses(Filters=filters)
        return response["Addresses"][1]
        
    return ""


# Get myvnp info from field
def getvpn_info(field: str) -> dict:
    resp = getvpn_address()
    if resp:
        return getvpn_address()[field]

    return {}
     

# Print myvnp address
def showvpn_address() -> None:
    out = getvpn_address()
    if out:
        print(out)
        return
    
    print("[w] No vpn instances detected!")
    return


def ssh_connect():
    # TODO: filter by tag in ec2 instance
    ip = getvpn_info("PublicIp")
    if ip:
        try:
            print(f"[i] SSH'ing into instance {ip}")
            subprocess.run(f"ssh admin@{ip}", shell=True, check=True)
        except Exception as e:
            print("[e] Failed to SSH into instance")
            raise e
        
        return 0
    
    print("[e] No instances detected!")


# Connect to myvnp instance via ssh
def ssm_connect():
    region = "eu-west-1" # TODO: do not hardcode
    idx = getvpn_info("InstanceId")
    if idx:
        try:
            print(f"[i] SSM'ing into target instance {idx}")
            subprocess.run(f"""aws ssm start-session --target "{idx}" --region {region}""", shell=True, check=True)
        except Exception as e:
            print("[e] Failed to SSM into instance")
            raise e
        return 0
    
    print("[e] No instances detected!")
    

# Connect to myvnp instance via ssm 
def ssm_exec(command: str) -> None:
    ssm = boto3.client('ssm', config=MYVPN_CONFG)    
    try:
        idx=getvpn_info("InstanceId")
        print(f"[i] SSM exec into target instance: {idx}")
        out = ssm.send_command(
            InstanceIds=[ idx ],
            DocumentName='AWS-RunShellScript', 
            Parameters={ "commands":[ f"{command}" ]  },
            Comment=f'myvpn command: {command}')
        
        print(f"ssm output:\n {out}" )
    except Exception as e:
        print("[e] Failed to SSM into instance")
        raise e


# Write ansible inventory file, optionally to a given destination 
def write_ansible_inventory(dest: Optional[str] = None, name: Optional[str] = None) -> None:
    import yaml

    hosts_dest = f'{os.getcwd()}' if dest is None else dest
    hosts_dest = f'{hosts_dest}/myvpnhosts' if dest is None else f'{hosts_dest}/{name}' 

    with open(hosts_dest, 'w') as ansible_inventory:
        # Default ansible inventory configuration for remote vpn and local machine
        inv = {"myvpn": 
                    { 
                        'vars': { 'ansible_ssh_user': ansible_ssh_user() },
                        'hosts':  getvpn_info('PublicIp')
                    },
                "local":
                    {   # TODO: setup local openssh install
                        # 'connection': 'local',
                        'hosts': 'localhost',
                    }
               }
        
        yaml.dump(inv, ansible_inventory)


# Configure openvpn between remote & local machines
def config_vpn(verbose: bool = False):
    # TODO: Setup openvpn between local & remote vpn... 
    # 1 sync config...
    # rsync -avL --progress -e "ssh -i ~/.ssh/id_rsa.pub" /tmp/mytesttodel/* admin@52.213.38.77:/tmp
    # 2 ssm exec ansible remote
    # 3 ansible local host 
    
    write_ansible_inventory()
    cmd = "ansible-playbook myvpn_playbook.yaml -i hosts-test"
    cmd = f"{cmd} --verbose" if verbose else cmd
    subprocess.run(cmd, shell=True, check=True)



