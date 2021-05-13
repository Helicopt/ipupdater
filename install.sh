#########################################################################
# File Name: install.sh
# Author: Toka
# mail: <empty>
# Created Time: Sat 08 May 2021 02:08:45 AEST
#########################################################################
#!/bin/bash


sudo cp ./upip.service /etc/systemd/system/upip.service
sudo mkdir -p /etc/upip
sudo cp ./upip/* /etc/upip/
sudo cp -r ./configs /etc/upip/
sudo chmod +x /etc/upip/exec

sudo apt-get install python3-pip
sudo -H python3 -m pip install pygsheets
sudo -H python3 -m pip install --upgrade six

sudo systemctl daemon-reload
sudo systemctl start upip.service
sudo systemctl enable upip.service


