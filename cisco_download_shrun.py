#!/usr/bin/env python

help="""
###############################################################################
# DevOps - Baixar a configuracao de todos os equipamentos que estão numa lista csv
# e salva num arquivo.cfg
# Filename: cisco_download_shrun.py
# Revision: 1.0
# Date: 24/09/2019
# Author: Diego Maia - diegosmaia@yahoo.com.br Telegram - @diegosmaia
###############################################################################
Executar o script passando o parametro do arquivo csv com a seguinte estrutura
user,pass,ip
admin,pass,10.201.0.22
###############################################################################


user@servidor:~/$ python cisco_download_shrun.py equipamentos.csv


"""

import netmiko
import time
import os
import datetime
import json
import re
import sys

import logging
#logging.basicConfig(filename='cisco_download_shrun.log', level=logging.DEBUG)
logging.basicConfig(filename='cisco_download_shrun.log', level=logging.INFO)

logger = logging.getLogger("netmiko")


#import argv to be able to call the csv file like 'python script.py devices.csv'
from sys import argv
#import csv module to be open to easily open and parse csv files.
import csv
#Import getpass so we can easily mask user input for passwords
import getpass

# Verificar se foi passados os comandos

if len(argv) < 2:
	print help
	exit ()
	
script, csv_file = argv


	
#now we want to define an object that contains our parsed csv file.
#we open the file with 'rb' tag (read binary) to ensure we get no funk formatting
reader = csv.DictReader(open(csv_file, 'rb'))

device_list = []


#takes our object we created from the parsed csv and makes a dict from each line
for line in reader:
		device_list.append(line)
				

for device in device_list:
		try:
				print('#'*79)
				print('Connection to Device', device['ip'])
				cisco_sw = {
								'device_type': 'cisco_ios',
								'host':		device['ip'],
								'username': device['user'],
								'password': device['pass'],
								'banner_timeout': 3,
								'auth_timeout': 3}
				connection = netmiko.ConnectHandler(**cisco_sw)
				filename = device['ip'] + '.conf'
				showrun = connection.send_command('show run', delay_factor=2)
				showvlan = connection.send_command('show vlan', delay_factor=2)
				showver = connection.send_command('show ver', delay_factor=2)
				config_file = open(filename, "w")		# in write mode
				config_file.write(showrun)
				config_file.write("\n")
				config_file.write(showvlan)
				config_file.write("\n")
				config_file.write(showver)
				config_file.write("\n")
				config_file.close()
				connection.cleanup()
				connection.disconnect()
				
		except Exception as e:
				print('Conexao falha: ' + device['ip'])
				print ('Falha: ' + str(e))


## switchport port-security
##	authentication open