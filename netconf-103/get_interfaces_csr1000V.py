#!/usr/bin/python
#
# Get interface operational state using NETCONF
#
# darien@sdnessentials.com
#

from interfaces import Interface
from ncclient import manager
import re
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
FILE = 'enable_odm_control.xml'


# create a method to retrieve interface operational data
def get_interface_state(host, port, user, passwd, filename):
    """Main method that retrieves the interfaces from config via NETCONF."""
    with manager.connect(host=host, port=port, username=user, password=passwd,
                         hostkey_verify=False, device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        # open the XML file to enable ODM
        with open(filename) as f:
            try:
                # issue the edit-config operation with the XML config to enable operational data
                rpc_reply = m.edit_config(target='running', config=f.read())
            except Exception as e:
                print("Encountered the following RPC error!")
                print(e)
                sys.exit()

        # verify ODM is enabled before continuing
        if rpc_reply.ok is not True:
            print("Encountered a problem when enabling ODM!")
            sys.exit()

        try:
            # issue the an RPC get while on interfaces-state
            rpc_reply = m.get(filter=('subtree', "<interfaces-state/>"))
        except Exception as e:
            print("Encountered the following RPC error!")
            print(e)
            sys.exit()

        # verify the RPC get was successful before continuing
        if rpc_reply.ok is not True:
            print("Encountered a problem when retrieving operational state!")
            sys.exit()
        else:
            # return the RPC reply containing interface data in XML format
            return(rpc_reply)


def main():
    """Simple main method calling our function."""
    list_interfaces = []
    result = get_interface_state(HOST, PORT, USER, PASS, FILE)
    print(xml.dom.minidom.parseString(result.xml).toprettyxml())
    # get a list of interfaces by parsing for the <interface> element
    interfaces = xml.dom.minidom.parseString(result.xml).getElementsByTagName('interface')
    # iterate over each instance of the <interface> element
    for each in interfaces:
        # parse out the <name> and <oper-status> nodes when the
        # <name> text node contains "GigabitEthernet|FastEthernet"
        if re.match('(Gigabit|Fast)Ethernet', each.getElementsByTagName('name')[0].firstChild.nodeValue):

            # instantiate an Interface() object for each instance of an interface
            interface = Interface(each.getElementsByTagName('name')[0].firstChild.nodeValue,
                                  each.getElementsByTagName('oper-status')[0].firstChild.nodeValue)
            list_interfaces.append(interface)

    # call the prints() method to print the interface data
    for each in list_interfaces:
        each.prints()

    # call the check_down() method to print each down interface and a warning
    for each in list_interfaces:
        each.check_down()


if __name__ == '__main__':
    sys.exit(main())
