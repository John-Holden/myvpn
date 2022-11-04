import boto3
import subprocess


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


def ssh_connect():
        # TODO: filter by tag in ec2 instance
    try:
        ec2 = boto3.client('ec2', region_name="eu-west-1")
        filters = [
            {'Name': 'domain', 'Values': ['vpc']}
        ]
        response = ec2.describe_addresses(Filters=filters)
        ip = response["Addresses"][1]["PublicIp"]
        print(f"[i] SSH'ing into instance {ip}")
        subprocess.run(f"ssh admin@{ip}", shell=True, check=True)
    except Exception as e:
        print("[e] Failed to SSH into instance")
        raise e

def server_vpn_setup():
    print("here")



