#!/usr/bin/python3

import argparse
import launcher_methods as lm

parser = argparse.ArgumentParser(description='Launch vpn to the cloud.')

parser.add_argument('--create',
                    required=False,
                    action='store_true',
                    help='sum the integers (default: find the max)')

parser.add_argument('--destroy',
                    required=False,
                    action='store_true',
                    help='destory your server')

parser.add_argument('--ssh',
                    required=False,
                    action='store_true',
                    help='ssh into your instance')

parser.add_argument('--server-config',
                    required=False,
                    action='store_true',
                    help='configure your server')


args = parser.parse_args()

lm.ssh_connect() if args.ssh else None
lm.create_instance() if args.create else None
lm.destroy_instance() if args.destroy else None
lm.server_vpn_setup() if args.server_vpn_setup else None