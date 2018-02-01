#!/bin/bash
#connect to raspberryPi via ethernet connection
# desktop enp3s0 enp0s25
ethernetInterface=enp3s0

if [ "$#" -eq 1 ]
then
    ethernetInterface=$1
fi

echo "Ethernet Interface: $ethernetInterface"
BcastAddr=`/sbin/ifconfig $ethernetInterface | grep "Bcast" | awk -F: '{print $3}' | awk '{print $1}'`
echo "Bcast Addr: $BcastAddr"
rpiAddr=`nmap -n -sP $BcastAddr/24 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'`
echo -e "Possible Raspberry Pi Address:\n$rpiAddr"