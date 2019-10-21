#!/usr/bin/env python

help="""
###############################################################################
# DevOps - Verifica em todos os arquivos .conf quais interfaces estao com 
# authentication open e falta de port-security
# Filename: check_port_security.py 
# Revision: 1.0
# Date: 24/09/2019
# Author: Diego Maia - diegosmaia@yahoo.com.br Telegram - @diegosmaia
###############################################################################

user@servidor:~/$ python check_port_security.py


"""

import time
import os
import datetime
import re
import sys
#Cisco http://www.pennington.net/py/ciscoconfparse/intro.html#what-is-ciscoconfparse-good-for
from ciscoconfparse import CiscoConfParse

from sys import argv
#import csv module to be open to easily open and parse csv files.
import csv
import re

import os

path = '.'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
		for file in f:
				if '.conf' in file:
						files.append(os.path.join(r, file))
						

csv_file = 'check_port_security.csv'
file_csv = open(csv_file, 'w')
try:
		writer = csv.writer(file_csv,
												dialect='excel',
												lineterminator = '\r\n',
												delimiter=';',
                        quotechar='"',
												quoting=csv.QUOTE_ALL)
		writer.writerow( ('HOSTNAME','IP', 'PORTA', 'TIPO_FALHA','INTERFACE_CONFIG') )
		for config_file in files:			
			confparse = CiscoConfParse(config_file)
			sw_hostname = confparse.re_match_iter_typed(r'^hostname\s+(\S+)', default='')
			sw_ip = (re.findall(r'\d+\.\d+\.\d+\.\d+',config_file))[0]
			
			security_intfs = confparse.find_objects_w_child(parentspec=r"^interf", childspec=r"authentication open")
			for result in security_intfs:
					security_intfs_2 = confparse.find_objects_w_child(parentspec=r"^"+result.text+'$', childspec=r"switchport mode access")
					for result_2 in security_intfs_2:
							config_porta = ""
							config_porta_obj = confparse.find_all_children(r'^'+result_2.text+'$')
							for linha in config_porta_obj:
									if config_porta == "":
										config_porta = linha +"\n"
									else:
										config_porta += linha +"\n"
					
							writer.writerow( (sw_hostname,sw_ip, result_2.text, 'Authentication Open',config_porta) )
			
			
			
			security_intfs = confparse.find_objects_wo_child(parentspec=r"^interf", childspec=r"switchport port-security")
			for result in security_intfs:
					security_intfs_2 = confparse.find_objects_w_child(parentspec=r"^"+result.text+'$', childspec=r"switchport mode access")
					for result_2 in security_intfs_2:
							config_porta = ""
							config_porta_obj = confparse.find_all_children(r'^'+result_2.text+'$')
							for linha in config_porta_obj:
									if config_porta == "":
										config_porta = linha +"\n"
									else:
										config_porta += linha +"\n"
					
							writer.writerow( (sw_hostname,sw_ip, result_2.text, 'Switchport port-security',config_porta) )
 
finally:
		file_csv.close()
