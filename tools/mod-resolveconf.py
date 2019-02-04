#!/usr/bin/env python3
# swap your /etc/resolv.conf depending on arguments
# takes one argument, "localhost" or "system"
# mod-resolveconf.py localhost (point everything to localhost)
# mod-resolvconf.py system (revert everything to what DHCP or other sets)
# this can useful for running pi-hole as a local container for your DNS
# https://hobo.house/2018/02/27/block-advertising-with-pi-hole-and-raspberry-pi/

import sys
import shutil
import subprocess

if len(sys.argv[1:]) != 1:
    print ("## Requires 1 argument ##")
    print ("mod-resolveconf.py localhost|system")
    exit(1)

# if you choose localhost, check DNS is working first
if sys.argv[1] == "localhost":
    dns_command = 'dig @localhost hobo.house'
    try:
        subprocess.check_output(dns_command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        ret = e.returncode
        if ret != 0:
            print("Cannot do DNS lookups against your localhost pi-hole, quitting.")
            exit(1)

# backup /etc/resolv.conf then set it to 'localhost'
def main():
    if sys.argv[1] == "localhost":
        shutil.copy2('/etc/resolv.conf', '/tmp/resolv.conf.system')
        dns = 'nameserver localhost\n'
        resolvconf = '/etc/resolv.conf'
        editconflocal = open(resolvconf, 'w')
        editconflocal.write(dns)
        editconflocal.close()
        print ("Updating /etc/resolv.conf to localhost...")
        print ("-----------------")
        with open(resolvconf, 'r') as result:
            shutil.copyfileobj(result, sys.stdout)

# revert /etc/resolv.conf from backup if it exists
    if sys.argv[1] == "system":
        try:
            resolvconf = '/etc/resolv.conf'
            shutil.copy2('/tmp/resolv.conf.system', '/etc/resolv.conf')
            print ("Reverting %s back to /tmp/resolv.conf.system ..." % resolvconf)
            print ("-----------------")
            with open(resolvconf, 'r') as result:
                shutil.copyfileobj(result, sys.stdout)
        except IOError:
            print ("No /tmp/resolv.conf.system found, may be running defaults")


if __name__ == '__main__':
    main()
