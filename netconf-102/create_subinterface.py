#!/usr/bin/env python
#
# Create a VLAN interface on top of a physical interface
# given parameters in code as global vars
# and VLAN / prefix / interface names as arguments
#
# darien@sdnessentials.com
#

import argparse
from jinja2 import Environment
from jinja2 import FileSystemLoader
from ncclient import manager
import netaddr
import os.path
import re
import sys


HOST = 'ios-xe-mgmt.cisco.com'
PORT = 10000
USER = 'root'
PASS = 'C!sc0123'
BASE = 'GigabitEthernet'
INT_ID = '3'
FILE = 'create_subinterface.xml'
TEMPLATE = 'create_subinterface.j2'


def create_xml_config(interface_template, xml_file, interface, int_id, vlan, ip, mask):
    """Function to render XML document to configure interface from Jinja2."""
    # Use the Jinja2 template provided to create the XML config
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(interface_template)
    rendered = template.render(base=interface, interface_id=int_id,
                               vlan_id=vlan, ip=ip, subnet_mask=mask)

    # save the results to the XML file passed as an argument
    with open(xml_file, "wb") as f:
        f.write(rendered)

    # exit if the file hasn't been created
    if os.path.isfile(xml_file) is not True:
        print("Failed to create the XML config file!")
        sys.exit()


def create_vlan(host, port, user, password, interface, int_id, vlan, ip, mask, template, config):
    """Function to create a subinterface on CSR1000V."""
    intfc = re.compile(r'^(\D+)(\d+)$')
    m = intfc.match(interface + int_id)
    if m is None:
        print("Invalid interface name. Valid example: ", BASE)
        sys.exit()

    # create the XML configuration issued via NETCONF
    create_xml_config(template, config, interface, int_id, vlan, ip, mask)

    # open the NETCONF session
    with manager.connect(host=host, port=port, username=user, password=password,
                         hostkey_verify=False, device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(config) as f:
            try:
                # issue the edit-config operation with the XML config
                rpc_reply = m.edit_config(target='running', config=f.read())
            except Exception as e:
                print("Encountered the following RPC error!")
                print(e)
                sys.exit()

            # validate the RPC Reply returns "ok"
            if rpc_reply.ok is not True:
                print("Encountered a problem when configuring the device!")
                sys.exit()


def main():
    """Main method to configure a subinterface."""
    parser = argparse.ArgumentParser()
    parser.add_argument('vlan', help="VLAN number (1-4094)", type=int)
    parser.add_argument('prefix', help="IPv4 or IPv6 prefix")
    parser.add_argument('--template', '-t', default=TEMPLATE, help="Jinja2 template file name")
    parser.add_argument('--config', '-c', default=FILE, help="XML config file name")
    parser.add_argument('--interface', '-i', default=BASE, help="interface name to use")
    parser.add_argument('--id', '-d', default=INT_ID, help="interface ID to use")
    parser.add_argument('--user', '-u', default=USER, help="user name on remote host")
    parser.add_argument('--password', '-p', default=PASS, help="password on remote host")
    parser.add_argument('--port', '-P', default=PORT, help="port on remote host")
    parser.add_argument('--host', '-H', default=HOST, help="remote host")
    args = parser.parse_args()

    # check for valid VLAN ID
    if args.vlan < 1 or args.vlan > 4094:
        parser.print_usage()
        print("invalid VLAN ID %s" % str(args.vlan))
        sys.exit()

    # check for valid prefix
    try:
        ip = netaddr.IPNetwork(args.prefix)
    except netaddr.core.AddrFormatError as e:
        parser.print_usage()
        print(e)
        sys.exit()

    return create_vlan(args.host, args.port, args.user, args.password, args.interface,
                       args.id, args.vlan, ip.ip, ip.netmask, args.template, args.config)


if __name__ == '__main__':
    sys.exit(main())
