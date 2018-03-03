#!/bin/bash
# Kevin Turkington (Zainkai)
# gunzip --stdout raspbian.img.gz | sudo dd bs=4M of=/dev/sdb
bsOption=4M

IFS=' ' read -ra sdCards <<< $(fdisk -l | grep -oE '/dev/sd[a-z]' | sort -u)

#list out devices
iter=0
echo -e "devices:\n"
for card in "${sdCards[@]}"; do
	echo -e "$iter)\t$card"
	((iter++))
done

read -p "\nChoose a device to clone: " sdChoice


if [[ "$sdChoice" =~ ^[0-9]+$ ]]
then
	echo "Filename: (example: raspbian)"
	read -p "> " filename

	echo "backing up and compressing..."
	sudo dd bs=$bsOption if=${sdCards[$sdChoice]} | gzip > "$filename.img.gz"
	echo "Done"
	exit 0
else
	echo "exiting..."
	exit 0
fi


