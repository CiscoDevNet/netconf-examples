#!/usr/bin/python

# import the ncclient library
import logging
from ncclient import manager
import sys

# rootLogger = logging.getLogger('ncclient.transport.session')
# rootLogger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# rootLogger.addHandler(handler)

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

        hostname_filter = '''
                          <show xmlns="http://www.cisco.com/nxos:1.0">
                              <hostname>
                              </hostname>
                          </show>
                          '''

        result = m.get(('subtree', hostname_filter))
        # print(result.data)
        # print(dir(result.data_ele))
        # print(result.data.nsmap['mod'])
        # print(result.data.prefix)
        # print(result.data.getroot)
        print(result.data.nsmap)
        # ns = {'mod': 'http://www.cisco.com/nxos:1.0:vdc_mgr'}
        print(result.data.findtext('mod:hostname', result.data.nsmap))
        # print(result.data.findtext('mod:hostname', result.data.nsmap))

if __name__ == '__main__':
    sys.exit(main())
