#!/usr/bin/python
#Andrew Hannebrink

# This script "rest.py" is supposed to run once a week by a crontab command from the 'dhcplog' user. The script uses each mac address in the table 'tempMacs' from the database constructed by dhcplog.py to update the lease of every user who has received a dhcp ack in the last week. The script is set to update the expiration date of the lease of each user in tempMacs to a default of 180 days from the current time.

import requests
import getpass
import sys
import json
import time 
import sqlite3
import eventlet
import MySQLdb
import smtplib
import string
sys.path.append('/usr/local/etc/')
import dhcpcfg


#Change these variables to change the maximum lease time, the username and password to log into infoblox, and the full path name of the database that is updated everyday by dhcplog.py

#########################################################################    
maxLease = dhcpcfg.maxLease * 86400  # Maxlease * (1 day in epoch time) #
username = dhcpcfg.infobloxUser						#                    
password = dhcpcfg.infobloxPasswd                       		#
host = dhcpcfg.sqlHost							#
user = dhcpcfg.sqlUser							#
passwd = dhcpcfg.sqlPasswd						#
db = dhcpcfg.db								#
senderEmail = dhcpcfg.senderEmail					#
senderPassword = dhcpcfg.senderPassword					#
recipientEmails = dhcpcfg.recipientEmails				#
url = dhcpcfg.ibxUrl
#########################################################################

#These variables keep track of different errors and successful trials of the script for the diagnostic report at the end

getFailures = 0
jsonLoadFailures = 0
putFailures = 0
successes = 0


#Call updateSingleLease() once for every mac address in the table 'tempMacs' located in dhcpdb.db
def updateIB(sqdb):
	query = 'SELECT * FROM tempMacs'
	sqdb.execute(query)
	todaysMacs = sqdb.fetchall()
	i = 0.0
	size = len(todaysMacs)
	for row in todaysMacs:
		ma = row[1]
		updateSingleLease(ma)
		if i % 200 == 0.0:
			print i / size
			print "requests.get failures: " + str(getFailures)
			print "json.loads failures: " + str(jsonLoadFailures)
			print "requests.put failures: " + str(putFailures)
			print "successes: " + str(successes)
		i = i + 1
		print i

#Connect to infoblox using Restful web services and update lease times accordingly, so that each lease updated is 180 days from the current time
def updateSingleLease(macaddress):
	ibxUrl = url + 'macfilteraddress'
	payload = {'mac':macaddress,'filter':'CaptivePortal'}
	try:
		# If the below line fails, it's likely because infoblox blocks a certain number of concurrent https requests
		r = requests.get(ibxUrl, data=json.dumps(payload), auth=(username,password), verify=False)
	except:
		global getFailures
		getFailures += 1
		return
	try:
		# If the below line fails, it's likely because the returned json object is empty, throwing an array index out of bounds error
		obj_ref = json.loads(r.content)[0]['_ref']
	except:
		global jsonLoadFailures
		jsonLoadFailures += 1
		return
	# Try to update each macaddress that had a dhcp ack in the last week to have an infoblox lease expiring 180 days from right now
	try:
		newExp = time.time() + maxLease
		modify_exp = {u'expiration_time': int(newExp)}
		r = requests.put(url + obj_ref, verify=False, data=jsrn.dumps(modify_exp), auth =('brink',password))
		global successes
		successes += 1
	except:
		global putFailures
		putFailures += 1
		return
	

def main():

	startTime = time.time()
	#Open database
	try:
		conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
		conn.text_factory = str
		c = conn.cursor()	
	except:
		print 'error opening database...'
		#EMAIL SOMEONE
		sys.exit(-1)
	# Update infoblox for the dhcp acks of the last week
	try:
		updateIB(c)
		#EMAIL SOMEONE
	except:
		print 'Error updating infoblox leases in updateIB()'
		#EMAIL SOMEONE
		sys.exit(-1)
	#Drop tempMacs and re-make it as an empty table to be re-populated throughout the next week by dhcplog.py
	c.execute('''DROP TABLE tempMacs''')
	c.execute('''CREATE TABLE tempMacs (id INTEGER PRIMARY KEY AUTO_INCREMENT, macaddress CHAR(18) UNIQUE)''')
	# Close the database connection
	conn.commit()
	conn.close()
	# Print the final diagnostic report
	print "requests.get failures: " + str(getFailures)
	print "json.loads failures: " + str(jsonLoadFailures)
	print "requests.put failures: " + str(putFailures)
	endTime = time.time()

	txt = 'requests.get failures = ' + str(getFailures) + '\njson.loads failures = ' + str(jsonLoadFailures) + '\nrequests.put failures = ' + str(putFailures) + '\nsuccesses = ' + str(successes) + '\ntotal time = ' + str(endTime - startTime)
	msg = string.join(('From: Andrew Hannebrink', 'To: %s' % str(recipientEmails), 'Subject: Weekly rest.py Diagnostic Report', '', txt), '\r\n')
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(senderEmail, senderPassword)
	mail.sendmail(senderEmail, recipientEmails, msg)
	mail.close()


if __name__ == '__main__':
	sys.exit(main())
