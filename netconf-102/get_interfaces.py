#!/usr/bin/python
#
# Get configured interfaces using Netconf
#
# darien@sdnessentials.com
#
from ncclient import manager
import sys


HOST = '10.10.10.51'
PORT = 22
USER = 'admin'
PASS = 'cisco123'


# create a main() method
def get_configured_interfaces():
    """Main method that retrieves the hostname from config via Netconf (NXOS)."""
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'nexus'},
                         allow_agent=False, look_for_keys=False) as cisco_manager:

        interfaces_filter = '''
                          <show xmlns="http://www.cisco.com/nxos:1.0">
                              <interface>
                              </interface>
                          </show>
                          '''

        print(cisco_manager.get(('subtree', interfaces_filter)))


def main():
    """Simple main method calling our function."""
    interfaces = get_configured_interfaces()

    # print the json that is returned
    print(interfaces)

if __name__ == '__main__':
    sys.exit(main())
