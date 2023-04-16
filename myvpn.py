#!/usr/bin/python3

import argparse
import vpn_bin.launcher_methods as lm

parser = argparse.ArgumentParser(description='Launch a disponsable vpn to the cloud.')

parser.add_argument('--deploy',
                    required=False,
                    action='store_true',
                    help='deploy your vpn server via tf conf')

parser.add_argument('--init',
                    required=False,
                    action='store_true',
                    help='init tf config')

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

parser.add_argument('--ssm',
                    required=False,
                    action='store_true',
                    help='ssm into your vpn instance')

parser.add_argument('--exec',
                    type=str, 
                    required=False,
                    action='store', 
                    help='ssm exec a command inside your vpn instance')

parser.add_argument('--info',
                    required=False,
                    action='store_true',
                    help='View vpn info')

parser.add_argument('--config',
                    required=False,
                    action='store_true',
                    help='configure your vpn server')

parser.add_argument('--verbose',
                    required=False,
                    action='store_true',
                    help='Provides more output to debug')


args = parser.parse_args()

lm.ssh_connect() if args.ssh else None
lm.ssm_connect() if args.ssm else None
lm.ssm_exec(args.exec) if args.exec else None
lm.plan_vpn() if args.plan else None
lm.init_vpn() if args.init else None
lm.deploy_vpn() if args.deploy else None
lm.destroy_vpn() if args.destroy else None
lm.redeploy_vpn() if args.redeploy else None
lm.showvpn_address() if args.info else None
lm.config_vpn(args.verbose) if args.config else None