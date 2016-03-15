#!/usr/bin/python
#
# Get interface operational state using NETCONF
#
# darien@sdnessentials.com
#


class Interface(object):
    """Basic Interface object to store information."""
    def __init__(self, name, status):
        """
        Constructor for basic interface class.

        Parameters: name of interface and interface status.
        """
        # Instantiate an interface with the name and status
        self.name = name
        self.status = status

    def check_down(self):
        """Basic check if interface is down and if so print a warning."""
        if self.status == 'down':
            print('#############################################')
            print("Warning! Interface: {int_name} is DOWN!".format(int_name=self.name))
            print('#############################################')

    def prints(self):
        """Basic method to print self."""
        print("Interface: {int_name}         Status: {int_status}".format(int_name=self.name,
                                                                          int_status=self.status))
