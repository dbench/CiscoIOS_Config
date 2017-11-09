"""
1.  This scripts pulls in switches from the list1 csv file,  SSHs into each and configures the commands in the config_commands variable.


2.  Library used is netmiko and this script utilizes the net_connect.send_config_set function.

--  Version 1.0
--  Created by:  Dustin Bench, 8/25/17 

--  Version 1.1
--  Modified by:  Dustin Bench, 8/30/17 (Added a feature that will bypass an SSH Exception using a try/except block.)

--  Version 1.0
--  Modified by:  Dustin Benc, 11/9/17 (Dropping all code into a function for import ability)
"""

import sys
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException

def ios_conf():

    file = open('c:\python27\list1.csv', 'r')

    print '\n\n>>>>>>>>>>>>>>> All Switches Python Script<<<<<<<<<<<<<<<<<<<'
    print '\n'

    #Create configuration command variable
    config_commands = ['ntp server 10.10.10.10', 'end', 'wr mem']

    for line in file:
        #Create a list out of list1_Network_Switch_Report.csv
        switch_list = line.strip().split(',')
        #Place each line of list1 into a dictionary
        device_info = {}
        device_info['device_type'] = switch_list[1]
        device_info['ip'] = switch_list[2]
        device_info['username'] = switch_list[3]
        device_info['password'] = switch_list[4]
        #create python list that includes all of the items in the device_info dictionary
        all_devices = [device_info]
        # Loop through device_info and apply config_commands to each element
        for a_device in all_devices:
            try:
                net_connect = ConnectHandler(**a_device)
                output = net_connect.send_config_set(config_commands)
                print "\n\n>>>>>>>>>>>>>>> Device {0} <<<<<<<<<<<<<<<".format(a_device['device_type'])
                print output
            except SSHException:
                print "\n\n>>>>>>>>>>>>>>> Device {0} <<<<<<<<<<<<<<<".format(a_device['ip'])
                print 'Connection to device failed.  Please check TACACS configuration, exiting.'
                continue
                sys.exit()
        print ">>>>>>>>>> END <<<<<<<<<<"

    file.close()

    print "\n\n"
    print ">>>>>>>>>>>>>>>>>>>>>>>Script has completed.  Good Bye<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

