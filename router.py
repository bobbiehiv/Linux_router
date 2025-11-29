

# script to use Linux box as a router 
#
# ie. route packets from an ethernet NIC a Wireless NIC on the same Debain linux device
# This can also create and bring up and LAN and Bridge interface for a disconnected interface to join (althoug it still has some bugs)
# will require firewalld and NetworkManager

from subprocess import call                                         
import subprocess
import time

#call(['ip','a'])       # use for testing

call(['nmcli', 'con', 'show'])
nicout = input('\nWhat will be your output interface(use connection name)? ')   # copy and paste the Connection name of the NIC when runnning 

print(f'\nUsing {nicout} for output interface')

#call(['ip','a'])       # use for testing

call(['nmcli', 'con', 'show'])
nicin = input('\nWhat will be your input interface(use connection name)? ')     # copy and paste the connection name of the NIC when runnning 

print('\nUsing {nicin} for input interface')

print('\nTurning on ip forwarding...')

call('echo 1 > ip_forward', shell=True, cwd='/proc/sys/net/ipv4/')      # changes file ip_forward to '1' if its '0'

        ## Uncomment this if you would like to create a Dummy interface and brigde that you can tie the In interface too ## 

# Create a Dummy interface lan0 and link it to a bridge that is always up br0 
#
#print('Creating dummy interface lan0 for input interface..')
#
#time.sleep(1)
#
#call(['ip', 'link', 'add', 'name', 'lan0', 'type', 'dummy'])            # creates dummy interface
#
#gw_ip = input('Set Gateway IP with Cidr: ')                             # choose a gatewat ip
#
#gw_lan = f'ip addr add {gw_ip} dev lan0'                                # adds gateway IP to dummy interface and calls with next line
#
#call(gw_lan, shell=True)                                                   
#                               
#print('Setting lan0 to up, creating bridge as br0 and setting up, setting lan0s master to br0...')
#
#time.sleep(1)
#
#call(['ip', 'link', 'set', 'lan0', 'up'])                               # set the dummy interface up and bring up a new bridge interface to 
#
#call(['ip', 'link', 'add', 'name', 'br0', 'type', 'bridge'])            # tie LAN0 to 
#
#call(['ip', 'link', 'set', 'br0', 'up'])
#
#call(['ip', 'link', 'set', 'lan0', 'master', 'br0'])
#
#br0_gw = f'ip addr add {gw_ip} dev br0'
#
#call(br0_gw, shell=True)                                                # adds IP to br0

                                    ####                                        ####

input('\nPlease make sure both interfaces are up and connected and press [enter]\n....')

device_out = subprocess.check_output(
    ['nmcli', '-g', 'GENERAL.DEVICES', 'con', 'show', nicout],          # because nmcli uses connection name. this converts the 
    text=True                                                           # connection name to device name, for use in firewalld rules 
).strip()                                                               # ie nicin will now be device_in

device_in = subprocess.check_output(
    ['nmcli', '-g', 'GENERAL.DEVICES', 'con', 'show', nicin],
    text=True
).strip()

first_rule = f'firewall-cmd --direct --add-rule ipv4 nat POSTROUTING 0 -o {device_out} -j MASQUERADE'

print('\nEnabling Masquerading rule...')
time.sleep(1)

call(first_rule, shell=True)                                            # turns on Masquerading on the output interface

in_out = f'firewall-cmd --direct --add-rule ipv4 filter FORWARD 0 -i br0 -o {device_out} -j ACCEPT'
                                   
print('\nEnabling Nic-in to Nic-out rule...')                                   
time.sleep(1)

call(in_out, shell=True)                                                # sets the IN to OUT rule

out_in = f'firewall-cmd --direct --add-rule ipv4 filter FORWARD 0 -i {device_out} -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT'

print('\nEnabling Nic-out to Nic-in rule...')
time.sleep(1)

call(out_in, shell=True)                                                # sets the OUT to IN rule

gw = input('\nNew Gateway IP with CIDR: ')                              # asks for ipv4 gateway with CIDR 

gw_in = f"nmcli con mod '{nicin}' ipv4.address {gw}"                      

print(f'\nNow using {gw} as Gateway IP')

call(gw_in, shell=True)                                                 # adds ipv4 via NetworkMcon_nicout

call('systemctl reload NetworkManager', shell=True)

print('\nTo reverse changes please use norouter.py or simpley restart PC\n')

input('Press [enter] to exit...')

print()

