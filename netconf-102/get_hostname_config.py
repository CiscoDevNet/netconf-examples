#!/usr/bin/python

# import the ncclient library
from ncclient import manager
import sys

# the variables below assume the user is requesting
# access to a Nexus device running in VIRL in the
# DevNet Always On SandBox
# use the IP address or hostname of your Nexus device
HOST = '172.16.1.82'
# use the NETCONF port for your Nexus device
PORT = 22
# use the user credentials for your Nexus device
USER = 'cisco'
PASS = 'cisco'


# create a main() method
def main():
    """Main method that retrieves the hostname from config via NETCONF (NXOS)."""
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'nexus'},
                         allow_agent=False, look_for_keys=False) as m:

        command = {'show running-config'}
        # the exec_command() method accepts a set as an argument
        # the set contains the NX-OS commands to run
        # the method returns XML as data
        result = m.exec_command(command)
        # print(dir(result.data))
        print(type(result.xml))
        print(result.xml)

if __name__ == '__main__':
    sys.exit(main())
