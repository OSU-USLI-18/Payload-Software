#!/bin/bash
#connect to raspberryPi via ethernet connection
# desktop enp3s0 enp0s25
ethernetInterface=enp3s0
j=0

if [ "$#" -eq 1 ]
then
	ethernetInterface=$1
fi

echo "Ethernet Interface: $ethernetInterface"
BcastAddr=`/sbin/ifconfig $ethernetInterface | grep "Bcast" | awk -F: '{print $3}' | awk '{print $1}'`
echo "Bcast Addr: $BcastAddr"

#convert nmap values to array
IFS=' ' read -ra rpiAddr <<< $(nmap -n -sP $BcastAddr/24 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
echo -e "Possible Raspberry Pi Address:\n"
for i in "${rpiAddr[@]}"; do
	echo -e "$j)\t$i"
	((j++))
done

echo -e "\nSelect address to ssh into.\nexit - to exit program.\n# - to ssh into that address"
read -p "rpi address: " sshChoice
if [[ "$sshChoice" =~ ^[0-9]+$ ]]
then
	echo "ssh-ing into raspberry pi at addr: ${rpiAddr[$sshChoice]}"
	ssh -Y pi@${rpiAddr[$sshChoice]}
elif  [[ "$sshChoice" -eq "exit" ]]
then
	echo "exiting..."
	exit 0
else
	echo "invalid input."
fi


