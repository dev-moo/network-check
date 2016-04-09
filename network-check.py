#!/usr/bin/env python

import os
from time import sleep, strftime
import ConfigParser



def log_event(e):

	tstamp = strftime("%Y%m%d%H%M%S")
	
	print e
	
	f = open(os.path.dirname(os.path.abspath(__file__)) + '/log.txt', 'a')
	f.write('"' + str(tstamp) + '","' + str(e) + '"\r\n')
	f.close()


def Test_Connection(rIP, sendIP):
	return os.system("sudo ping -I " + sendIP + " -c 1 " + rIP)

	
def Restore_Connection(rIP, ip, name):
	
	log_event("Attempting restore 1 on interface " + name)
	os.system("sudo ifup " + name)

	sleep(10)
	
	if Test_Connection(rIP, ip) == 0:
		log_event("Restore successful on interface " + name)
		return True	
	else:
		log_event("Restore 1 failed on interface " + name)
		
		
	log_event("Attempting restore 2 on interface " + name)
	
	os.system("sudo ifdown " + name)
	sleep(10)
	os.system("sudo --force ifup " + name)

	if Test_Connection(rIP, ip) == 0:
		log_event("Restore successful on interface " + name)
		return True			
	else:
		log_event("Restore 2 failed on interface " + name)		
		

	log_event("Attempting restore 3 on interface " + name)
	os.system("sudo /etc/init.d/networking restart")

	sleep(10)
	
	if Test_Connection(rIP, ip) == 0:
		log_event("Restore successful on interface " + name)
		return True	
	else:
		log_event("Restore 3 failed on interface " + name)
		

	log_event("Attempting restore 4 on interface " + name)
	os.system("sudo /etc/init.d/networking reload")

	sleep(10)
	
	if Test_Connection(rIP, ip) == 0:
		log_event("Restore successful on interface " + name)
		return True	
	else:
		log_event("Restore 4 failed on interface " + name)
		
	
	#log_event("Attempting restore 3 (reboot) of Pi " + name)
	#os.system("sudo reboot")
		
	print "Restore failed :("
	
	return False
	
		
def Check_Interface(rIP, ip, name):
	
	if Test_Connection(rIP, ip) == 0:
		return True
	
	sleep(5)

	if Test_Connection(rIP, ip) == 0:
		return True	
		
	log_event("Ping failed on interface " + name)
	return False
		
		
	


		
if __name__ == "__main__":
		
	# Check config file exists	

	dir = os.path.dirname(os.path.abspath(__file__))
	filepath = dir + '/config.conf'

	if not os.path.isfile(filepath):
		print ("Error - Missing Config File: config.conf")
		quit()

	# Get config	
	config = ConfigParser.ConfigParser()
	config.read(filepath)

	
	lanEnabled = config.get('config', 'lanEnabled')	
	wlanEnabled = config.get('config', 'wlanEnabled')	
	routerIP = config.get('config', 'routerIP')	
	ethIP = config.get('config', 'ethIP')
	wlanIP = config.get('config', 'wlanIP')
	ethName = config.get('config', 'lanname')
	wlanName = config.get('config', 'wlanname')
		
	
	if lanEnabled == 'True':
		lanEnabled = True
	else:
		lanEnabled = False
	
	if wlanEnabled == 'True':
		wlanEnabled = True
	else:
		wlanEnabled = False
	
	print "Checking ethernet"
	if lanEnabled and Check_Interface(routerIP, ethIP, ethName) == False:
		Restore_Connection(routerIP, ethIP, ethName)
	else:
		print "Ethernet is up"
		
	print ""
	
	print "Checking WIFI"	
	if wlanEnabled and Check_Interface(routerIP, wlanIP, wlanName) == False:
		Restore_Connection(routerIP, wlanIP, wlanName)	
	else:
		print "WIFI is up"


