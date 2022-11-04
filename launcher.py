#!/usr/bin/python3

import argparse
import launcher_methods as lm

parser = argparse.ArgumentParser(description='Launch vpn to the cloud.')

parser.add_argument('--deploy',
                    required=False,
                    action='store_true',
                    help='deploy your vpn server')

parser.add_argument('--plan',
                    required=False,
                    action='store_true',
                    help='plan your vpn server')

parser.add_argument('--destroy',
                    required=False,
                    action='store_true',
                    help='destory your vpn server')

parser.add_argument('--redeploy',
                    required=False,
                    action='store_true',
                    help='destroy & rebuild your vpn server')

parser.add_argument('--ssh',
                    required=False,
                    action='store_true',
                    help='ssh into your vpn instance')

parser.add_argument('--server_config',
                    required=False,
                    action='store_true',
                    help='configure your vpn server')


args = parser.parse_args()

lm.ssh_connect() if args.ssh else None
lm.plan_vpn() if args.plan else None
lm.deploy_vpn() if args.deploy else None
lm.destroy_vpn() if args.destroy else None
lm.redeploy_vpn() if args.redeploy else None
lm.server_vpn_setup() if args.server_config else None