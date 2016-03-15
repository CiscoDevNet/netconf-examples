#!/usr/bin/python
#
# Get interface operational state using screen scraping
#
# darien@sdnessentials.com
#

from interfaces import Interface
import re
import sys


def main():
    """
    Open a file called show_ip_int_brie.txt.

    Parse through interface data and create an Interface object for each one found.
    """
    interfaces = []
    INTERFACE_REGEX = '^(FastEthernet|GigabitEthernet)([0-9]+) .*(up|down)'
    # open the file called 'show_ip_int_brief.txt'
    with open('show_ip_int_brief.txt', 'r') as interface_info:
        for line in interface_info:
            # Iterate over each line and match against the string INTERFACE_REGEX
            m = re.match(INTERFACE_REGEX, line)
            if m is not None:
                # When the line matches the REGEX, create an Interface() object
                interface = Interface(m.group(1) + m.group(2), m.group(3))
                # Append the interface to the list, so we can iterate over it
                interfaces.append(interface)

    # for each interface print the name and status
    for interface in interfaces:
        interface.prints()

    # call the check_down() function to print any interfaces in the down state with a warning
    for interface in interfaces:
        interface.check_down()

if __name__ == '__main__':
    sys.exit(main())
