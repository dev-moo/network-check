import os
import time

router = "192.168.1.1"
lan = "eth0"
wlan = "wlan0"

iplan = "192.168.1.2"
ipwlan = "192.168.1.3"

def lanUp (hostname):
	response = os.system("ping -I " + iplan + " -c 1 " + hostname)
	return response
	
def wlanUp (hostname):
        response = os.system("ping -I " + ipwlan + " -c 1 " + hostname)
        return response
	

if lanUp (router) != 0:
	os.system("sudo ifup " + lan)

time.sleep(5)

if lanUp (router) != 0:
	os.system("sudo ifdown " + lan)
	time.sleep(5)
	os.system("sudo ifup " + lan)



if wlanUp (router) != 0:
        os.system("sudo ifup " + wlan)

time.sleep(5)

if wlanUp (router) != 0:
        os.system("sudo ifdown " + wlan)
        time.sleep(5)
        os.system("sudo ifup " + wlan)

