#####################################################
# Define providers
#####################################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


# Configure the AWS Provider
provider "aws" {
  region = "eu-west-1"
}

# #####################################################
# # Define base networking, vpc & subnets
# #####################################################

resource "aws_vpc" "main" {
  cidr_block = "172.16.0.0/16"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main"
  }
}

resource "aws_subnet" "sb_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "172.16.10.0/24"
  availability_zone = "eu-west-1a"
}

resource "aws_subnet" "sb_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "172.16.11.0/24"
  availability_zone = "eu-west-1b"
}

resource "aws_route_table" "allow" {
  vpc_id = aws_vpc.main.id

  route { ## update to be your ip
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "allow-ssh"
  }
}

resource "aws_route_table_association" "sb_a_rta" {
  subnet_id      = aws_subnet.sb_a.id
  route_table_id = aws_route_table.allow.id
}

####################################################
# ALB routes incoming traffic to EC2
####################################################

resource "aws_instance" "webserver" {
ami                  = "ami-0aca9de1791dcec2a" // Deb-11
instance_type        = "t2.micro"
subnet_id            =  aws_subnet.sb_a.id
key_name             =  aws_key_pair.ssh_key.key_name
user_data            = file("../include/vpn_bootstrap.sh")
iam_instance_profile = "${aws_iam_instance_profile.myvpn.id}"
tags          = {
    name        = "myvpn",
  }
root_block_device {
    volume_size = 20
  }
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "ssh-key"
  public_key = var.public_ssh
  }

resource "aws_network_interface" "web_interface" {
  subnet_id   = aws_subnet.sb_a.id
}

resource "aws_eip" "ssh_ip" {
 vpc      = true
 instance = aws_instance.webserver.id
}

###################################################
# SSH security groups
####################################################

resource "aws_security_group" "allow_ssh" {
name = "allow-all-sg"
vpc_id = aws_vpc.main.id

# Allow SSH
ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

# Allow SSM
ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

# Allow SSM
egress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    cidr_blocks = [
    "0.0.0.0/0"
    ]
  }

# Allow OpenVpn
ingress {
    from_port = 1194
    to_port   = 1194
    protocol  = "udp"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

# Allow OpenVpn
egress {
    from_port = 1194
    to_port   = 1194
    protocol  = "udp"
    cidr_blocks = [
    "0.0.0.0/0"
    ]
  }
}

resource "aws_network_interface_sg_attachment" "sg_attachment" {
  security_group_id    = aws_security_group.allow_ssh.id
  network_interface_id = "${aws_instance.webserver.primary_network_interface_id}"
}

###################################################
# IAM policy for SSM
####################################################
resource "aws_iam_instance_profile" "myvpn" {
  name = "myvpn"
  role = aws_iam_role.role.name
}

resource "aws_iam_role_policy_attachment" "myvnp-attach" {
  role       = aws_iam_role.role.name
  # The default ssm policy
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role" "role" {
  name = "myvpn"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}