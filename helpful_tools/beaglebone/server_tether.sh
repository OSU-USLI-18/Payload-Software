#!/bin/bash

# run this on the computer first
ifconfig enx38d269442378 192.168.7.1
iptables --table nat --append POSTROUTING --out-interface enp3s0 -j MASQUERADE
iptables --append FORWARD --in-interface enx38d269442378 -j ACCEPT
echo 1 > /proc/sys/net/ipv4/ip_forward
