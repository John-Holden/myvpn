import boto3
import subprocess
from botocore.config import Config

# TODO: mk this part of user config etc.
myvpn_config = Config(
    region_name = 'eu-west-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)


def plan_vpn():
    print("[i] Planning instance from tf configuration...")
    subprocess.run("terraform plan -var-file=my.tfvars", shell=True, check=True)
    return True

def deploy_vpn():
    print("[i] Creating instance from tf configuration...")
    subprocess.run("terraform apply -var-file=my.tfvars", shell=True, check=True)
    return True


def destroy_vpn():
    print("[i] Destroying instance from tf configuration...")
    subprocess.run("terraform destroy -var-file=my.tfvars", shell=True, check=True)
    return True

def redeploy_vpn():
    print("[i] Redploying your vpn instance...")
    subprocess.run("terraform destroy -target=aws_instance.webserver -var-file=my.tfvars", shell=True, check=True)
    subprocess.run("terraform apply -var-file=my.tfvars", shell=True, check=True)

def getvpn_address():
    ec2 = boto3.client('ec2', region_name="eu-west-1")
    filters = [ {'Name': 'domain', 'Values': ['vpc']} ]
    response = ec2.describe_addresses(Filters=filters)
    return response["Addresses"][1]


def getvpn_info(field: str):
    return getvpn_address()[field]


def showvpn_address():
    return print(getvpn_address())


def ssh_connect():
        # TODO: filter by tag in ec2 instance
    try:
        ip = getvpn_info("PublicIp")        
        print(f"[i] SSH'ing into instance {ip}")
        subprocess.run(f"ssh admin@{ip}", shell=True, check=True)
    except Exception as e:
        print("[e] Failed to SSH into instance")
        raise e


def ssm_connect():
    region = "eu-west-1" # TODO: do not hardcode
    try:
        idx = getvpn_info("InstanceId")        
        print(f"[i] SSM'ing into target instance {idx}")
        subprocess.run(f"""aws ssm start-session --target "{idx}" --region {region}""", shell=True, check=True)
    except Exception as e:
        print("[e] Failed to SSM into instance")
        raise e


def ssm_exec(command: str):
    ssm = boto3.client('ssm', config=myvpn_config)    
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


def config_vpn():
    import ansible_runner
    # TODO: Setup openvpn between local & remote vpn... 
    print("here")


