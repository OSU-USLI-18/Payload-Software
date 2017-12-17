#!/bin/bash

# run this on server
# to get interfaces run ifconfig

#server web connected interface
serverweb="enp3s0"
#beaglebone usb interface
bbbInterface="enx38d269442378"

ifconfig $bbbInterface 192.168.7.1
iptables --table nat --append POSTROUTING --out-interface $serverweb -j MASQUERADE
iptables --append FORWARD --in-interface $bbbInterface -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward
