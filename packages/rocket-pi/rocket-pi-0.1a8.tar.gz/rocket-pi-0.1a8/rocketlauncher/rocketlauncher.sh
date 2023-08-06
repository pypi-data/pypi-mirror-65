#!/bin/bash

# Project skidloader
# This is the script required for autostarting
# all dependent executables
# and is getting called by rocket.services launcher
# at the boot time

# Author: Martin Shishkov
# Created : 05.03.2020
#

sudo nohup dhcpcd -d
echo "access point ip address granted" 
nohup ./RIB_App&
echo "RIB started"
nohup webiopi -c /etc/webiopi/config&
echo "provider app started"
nohup ./Digger_Consumer_App&
echo "consumer app started"
exit 0
