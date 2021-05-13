#########################################################################
# File Name: uninstall.sh
# Author: Toka
# mail: <empty>
# Created Time: Sat 08 May 2021 02:13:28 AEST
#########################################################################
#!/bin/bash


sudo systemctl stop upip.service
sudo systemctl disable upip.service

sudo rm /etc/systemd/system/upip.service

sudo systemctl daemon-reload


