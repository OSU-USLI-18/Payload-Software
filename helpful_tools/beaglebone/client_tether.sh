#!/bin/bash

# run this on the beaglebone after running the "server" side script
ifconfig usb0 192.168.7.2
route add default gw 192.168.7.1
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
# getting the time
ntpdate -b -s -u pool.ntp.org
