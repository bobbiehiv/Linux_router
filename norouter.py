

# script to stop using your Linux box as a router 
# Flushes all firewall rules and resets NIC to DHCP
# will need firewalld and NetworkManager

from subprocess import call
import sys
import time

reset_FW = input('Reset all firewall rules to default? (yes/no): ')

if reset_FW.lower() == 'yes':
    
    print('Resetting firewall to defaults...')      # will reset firewalld to defaults and reload
    
    call('firewall-cmd --reset-to-defaults', shell=True)
    
    time.sleep(1)
    
    call('firewall-cmd --reload', shell=True)

    reset_GW = input('Reset gateway address on an interface? (yes/no): ')

    if reset_GW.lower() == 'yes':
        call(['nmcli', 'con', 'show'])
        
        nicin = input('\nWhich interface? ')          # copy and paste the connection name of the NIC

        gw_in = f"nmcli con mod '{nicin}' ipv4.address ''"
        
        call(gw_in, shell=True)
        
        call('systemctl reload NetworkManager', shell=True)

        print(f'Cleared static IPv4 address on {nicin}')
    else:
        print('Ok,\nExiting...')
        sys.exit()

