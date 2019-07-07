# Overview

RHOME Open Hack Challenge SensorMedal Client application.


# Usage

## install library

'''
$ sudo pip3 install bluepy
'''

## Run

Set your SensorMedal name list as argument of get_medal_data func in app.py

'''python
medals = get_medal_data(['ROHMMedal2_0073_01.00'])
'''

'''
 sudo python3 /tmp/pycharm_project_378/app.py --private_key_file=/home/pi/rsa_private.pem --my-config=/tmp/pycharm_project_378/medal_client.conf  --ca_certs_file=/home/pi/roots.pem
'''


