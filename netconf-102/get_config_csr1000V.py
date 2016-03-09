#!/usr/bin/python
#
# Get configured interfaces using Netconf
#
# darien@sdnessentials.com
#

from ncclient import manager
import sys
import xml.dom.minidom


# the variables below assume the user is requesting access
# to a IOS-XE device running in the DevNet Always On SandBox
# use the IP address or hostname of your IOS-XE device
HOST = 'ios-xe-mgmt.cisco.com'
# use the NETCONF port for your IOS-XE device
PORT = 10000
# use the user credentials for your IOS-XE device
USER = 'root'
PASS = 'C!sc0123'
# XML file to open
FILE = 'get_interfaces.xml'


# create a main() method
def get_configured_interfaces():
    """Main method that retrieves the interfaces from config via NETCONF."""
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        with open(FILE) as f:
            return(m.get_config('running', f.read()))


def main():
    """Simple main method calling our function."""
    interfaces = get_configured_interfaces()
    print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())


if __name__ == '__main__':
    sys.exit(main())
