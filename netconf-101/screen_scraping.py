#!/usr/bin/python

import re
import sys


def main():
    """
    Open a file called sandbox-nexus9kv-config.txt.
    Print each line that matches a regular expression for a hostname route.
    """
    HOSTNAME = ''
    NXOS_HOSTNAME_REGEX = '^hostname (.*)$'
    NXOS_DOMAIN_REGEX = '^ip domain-name (.*)$'
    with open('sandbox-nexus9kv-config.txt', 'r') as nexus_config:
        for line in nexus_config:
            if re.match(NXOS_HOSTNAME_REGEX, line):
                HOSTNAME = re.search(NXOS_HOSTNAME_REGEX, line).group(1) + '.'
            elif re.match(NXOS_DOMAIN_REGEX, line):
                HOSTNAME += re.search(NXOS_DOMAIN_REGEX, line).group(1)

    print(HOSTNAME)

if __name__ == '__main__':
    sys.exit(main())
