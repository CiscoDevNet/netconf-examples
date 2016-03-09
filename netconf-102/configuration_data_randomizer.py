#!/usr/bin/env python
#
# Randomize a VLAN ID and address to run
# create_subinterface.py against the CSR1000V
# in the Always On SandBox
#
# darien@sdnessentials.com
#

import argparse
import netaddr
import random
import sys


# base prefix to pick random address
ADDR_BASE = '1.0.0.0/20'
# base prefix to pick random route
ROUTE_BASE = '1.1.0.0/20'
# prefix length of resulting random route
LENGTH = 31


def random_vlan():
    """Return random VLAN ID."""
    return random.choice(range(1, 4095))


def random_address(base):
    """Return a random address based on a base prefix."""
    prefix = netaddr.IPNetwork(base)
    addresses = netaddr.IPSet(prefix)
    for address in [prefix.network, prefix.broadcast]:
        addresses.remove(address)
    return str(random.choice(list(addresses))) + '/' + str(prefix.prefixlen)


def random_route(base, length):
    """Return a random route based on a base prefix and target prefix length."""
    ip = netaddr.IPNetwork(base)
    routes = list(ip.subnet(length))
    return random.choice(routes)


def main():
    """Main method to randomize example configuration data."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr_base', '-a', default=ADDR_BASE, help="base prefix to pick address")
    parser.add_argument('--route_base', '-r', default=ROUTE_BASE, help="base prefix to subnet")
    parser.add_argument('--length', '-l', default=LENGTH, help="prefix length of resulting subnets", type=int)
    args = parser.parse_args()
    print('################################################')
    print('Here is an example way to run the script: ')
    print("python create_subinterface.py {v} {a}".format(v=random_vlan(), a=random_address(args.addr_base)))
    print('################################################')


if __name__ == '__main__':
    sys.exit(main())
