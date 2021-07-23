#!/bin/bash
sudo mkdir /home/ec2-user/perryrhodan
sudo wget https://lab2-huy.s3-us-west-1.amazonaws.com/perryrhodan.py -P /home/ec2-user/perryrhodan
sudo chown -R ec2-user /home/ec2-user/perryrhodan
sudo wget https://lab2-huy.s3-us-west-1.amazonaws.com/perryrhodan.service -P /etc/systemd/system
sudo systemctl enable perryrhodan; systemctl start perryrhodan
pip3 install mysql-connector
sudo yum update -y
sudo yum install -y mariadb-server
sudo systemctl start mariadb

