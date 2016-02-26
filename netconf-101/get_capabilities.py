#!/usr/bin/env python

import logging
from ncclient import manager
import sys


# the variables below assume the user is requesting access to a
# Nexus device running in VIRL in the  DevNet Always On Sandbox
# use the IP address or hostname of your Nexus device
HOST = '172.16.1.82'
# use the NETCONF port for your Nexus device
PORT = 22
# use the user credentials for your Nexus device
USER = 'cisco'
PASS = 'cisco'


# create a main() method
def main():
    """Main method that prints NETCONF capabilities of remote device."""
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # print all NETCONF capabilities
        print('***Here are the Remote Devices Capabilities***')
        for capability in m.server_capabilities:
            print(capability)

if __name__ == '__main__':
    sys.exit(main())
