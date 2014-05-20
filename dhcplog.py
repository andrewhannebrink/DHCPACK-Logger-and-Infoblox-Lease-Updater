#!/usr/bin/python

# This script parses the infoblox log file /var/log/infoblox.log.1 each day when called by the dhcplog user's crontab file. Each line of the file is matched with a regular expression describing a line that logs a DHCPACK event. When there is a match, the script records the date, the clients IP address, the clients mac address, and the client's hostname. The script then stores this information to a database whose default path is /

#What follows is sample content from /var/log/infoblox.log.1

#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 172.27.8.149 from 18:af:61:65:ea:a2 (iPhone) via 172.27.8.252 (RENEW)
#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPACK on 172.27.8.149 to 18:af:61:65:ea:a2 (iPhone) via eth1 relay 172.27.8.252 lease-duration 86400 (RENEW)
#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 172.27.8.149 from 18:af:61:65:ea:a2 (iPhone) via 172.27.8.253 (RENEW)
#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPACK on 172.27.8.149 to 18:af:61:65:ea:a2 (iPhone) via eth1 relay 172.27.8.253 lease-duration 86400 (RENEW)
#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.19.16.49 via 172.19.17.254
#Aug  6 09:07:29 128.252.0.1 dhcpd[7578]: DHCPACK to 172.19.16.49 (78:2b:cb:b1:47:cd) via eth1
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPREQUEST for 172.25.94.166 from 00:25:4b:b1:69:ce (IMAC0949W) via eth1 (RENEW)
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPACK on 172.25.94.166 to 00:25:4b:b1:69:ce (IMAC0949W) via eth1 relay eth1 lease-duration 30 (RENEW)
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: BOOTREQUEST from 00:c0:b7:2b:0e:1b via 128.252.12.190: BOOTP from dynamic client and no dynamic leases
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPDISCOVER from 00:0c:e6:07:a8:e5 via 172.20.202.254: network 172.20.202.0/24: no free leases
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: Hostname BME240-Nerva replaced by BME240-Nerva
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPINFORM from 172.16.20.18 via 172.16.21.254
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPACK to 172.16.20.18 (00:13:72:1a:2f:63) via eth1
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: Hostname android-fa673f693ba0fc65 replaced by android-fa673f693ba0fc65
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: uid lease 172.25.20.111 for client cc:3a:61:bf:e0:e5 is duplicate on vl394-captive-portal
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: Hostname android-fa673f693ba0fc65 replaced by android-fa673f693ba0fc65
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: uid lease 172.25.20.111 for client cc:3a:61:bf:e0:e5 is duplicate on vl394-captive-portal
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPOFFER on 172.25.20.111 to cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via eth1 relay 172.26.63.252 lease-duration 120
#Aug  6 09:07:30 128.252.0.17 dhcpd[310]: DHCPDISCOVER from 00:25:90:77:4d:1d via 128.252.125.254: network physics: no free leases
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: BOOTREQUEST from 00:c0:b7:2b:0e:1b via 128.252.12.190: BOOTP from dynamic client and no dynamic leases
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPDISCOVER from 00:0c:e6:07:a8:e5 via 172.20.202.254: network 172.20.202.0/24: no free leases
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 172.25.108.25 from 64:27:37:4f:58:74 (MOSTLBA142295) via eth1 (RENEW)
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPACK on 172.25.108.25 to 64:27:37:4f:58:74 (MOSTLBA142295) via eth1 relay eth1 lease-duration 30 (RENEW)
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: Hostname BME240-Nerva replaced by BME240-Nerva
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.16.20.18 via 172.16.21.254
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPACK to 172.16.20.18 (00:13:72:1a:2f:63) via eth1
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPOFFER on 172.25.2.0 to cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via eth1 relay 172.26.63.252 lease-duration 120
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: Hostname android-fa673f693ba0fc65 replaced by android-fa673f693ba0fc65
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 172.25.2.0 (128.252.0.1) from cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via 172.26.63.252
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPACK on 172.25.2.0 to cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via eth1 relay 172.26.63.252 lease-duration 30
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: Hostname android-fa673f693ba0fc65 replaced by android-fa673f693ba0fc65
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 172.25.2.0 (128.252.0.1) from cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via 172.26.63.253 (RENEW)
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPACK on 172.25.2.0 to cc:3a:61:bf:e0:e5 (android-fa673f693ba0fc65) via eth1 relay 172.26.63.253 lease-duration 30 (RENEW)
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: Added new forward map from android-fa673f693ba0fc65.dhcp.wustl.edu to 172.25.2.0
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: Added reverse map from 0.2.25.172.in-addr.arpa. to android-fa673f693ba0fc65.dhcp.wustl.edu
#Aug  6 09:07:30 128.252.0.1 dhcpd[7578]: DHCPDISCOVER from 00:25:90:77:4d:1d via 128.252.125.254: network physics: no free leases
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPEXPIRE on 172.27.38.125 to 0c:84:dc:87:88:6e
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Removed forward map from narmstro.dhcp.wustl.edu to 172.27.38.125
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Removed reverse map on 125.38.27.172.in-addr.arpa.
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.18.203.232 via 172.18.203.252
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 172.18.203.232 (6c:88:14:b6:53:84) via eth1
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 172.18.203.232 via 172.18.203.252
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 172.18.203.232 (6c:88:14:b6:53:84) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.18.203.232 via 172.18.203.253
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 172.18.203.232 (6c:88:14:b6:53:84) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 172.18.203.232 via 172.18.203.253
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 172.18.203.232 (6c:88:14:b6:53:84) via eth1
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname lib-ref2 replaced by lib-ref2
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 128.252.66.84 via 128.252.66.252
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 128.252.66.84 (f0:1f:af:26:dd:52) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.66.84 via 128.252.66.252
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.66.84 (f0:1f:af:26:dd:52) via eth1
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname RMS-Reg replaced by RMS-Reg
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname RMS-Reg replaced by RMS-Reg
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname RMS-Reg replaced by RMS-Reg
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname RMS-Reg replaced by RMS-Reg
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 192.168.0.204 from a0:b3:cc:fc:c4:a0 via 192.168.1.254: ignored (unknown subnet).
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPREQUEST for 192.168.0.204 from a0:b3:cc:fc:c4:a0 via 192.168.1.254: ignored (unknown subnet).
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname Bixby_Admin_Office-PC replaced by Bixby_Admin_Office-PC
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname Bixby_Admin_Office-PC replaced by Bixby_Admin_Office-PC
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 128.252.92.140 via 128.252.157.254
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 128.252.92.140 (00:1f:29:01:d5:72) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.92.140 via 128.252.157.254
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.92.140 (00:1f:29:01:d5:72) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname CC-036060 replaced by CC-036060
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.159.33 via 128.252.159.254
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.159.33 (00:21:70:14:5d:79) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname android-2f6834f3730be47f replaced by android-2f6834f3730be47f
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPREQUEST for 192.168.1.85 from e0:75:7d:67:72:d1 via 172.26.63.252: wrong network.
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPNAK on 192.168.1.85 to e0:75:7d:67:72:d1 via 172.26.63.252
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname CC-036060 replaced by CC-036060
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname android-2f6834f3730be47f replaced by android-2f6834f3730be47f
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 128.252.159.33 via 128.252.159.254
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPREQUEST for 192.168.1.85 from e0:75:7d:67:72:d1 via 172.26.63.253: wrong network.
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 128.252.159.33 (00:21:70:14:5d:79) via eth1
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPNAK on 192.168.1.85 to e0:75:7d:67:72:d1 via 172.26.63.253
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 172.16.28.25 via 172.16.29.254
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname android-2f6834f3730be47f replaced by android-2f6834f3730be47f
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 192.168.1.85 from e0:75:7d:67:72:d1 via 172.26.63.252: wrong network.
#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 172.16.28.25 (78:2b:cb:ae:be:c2) via eth1
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPNAK on 192.168.1.85 to e0:75:7d:67:72:d1 via 172.26.63.252
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: Hostname android-2f6834f3730be47f replaced by android-2f6834f3730be47f
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPREQUEST for 192.168.1.85 from e0:75:7d:67:72:d1 via 172.26.63.253: wrong network.
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPNAK on 192.168.1.85 to e0:75:7d:67:72:d1 via 172.26.63.253
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.16.28.25 via 172.16.29.254
#Aug  6 09:07:31 128.252.0.1 dhcpd[7578]: DHCPACK to 172.16.28.25 (78:2b:cb:ae:be:c2) via eth1
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: Hostname BAMCO-D003 replaced by BAMCO-D003
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPINFORM from 172.21.0.97 via 172.21.0.126
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPACK to 172.21.0.97 (d4:be:d9:d5:55:83) via eth1
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: Hostname BAMCO-D003 replaced by BAMCO-D003
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: DHCPINFORM from 172.21.0.97 via 172.21.0.126
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: DHCPACK to 172.21.0.97 (d4:be:d9:d5:55:83) via eth1
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPREQUEST for 172.25.95.158 from 00:25:4b:b1:1b:9c (IMAC0947W) via eth1 (RENEW)
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPACK on 172.25.95.158 to 00:25:4b:b1:1b:9c (IMAC0947W) via eth1 relay eth1 lease-duration 30 (RENEW)
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: Hostname AD-L088 replaced by AD-L088
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: Hostname AD-L088 replaced by AD-L088
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: DHCPINFORM from 128.252.96.114 via 128.252.97.254
#Aug  6 09:07:32 128.252.0.1 dhcpd[7578]: DHCPACK to 128.252.96.114 (f0:de:f1:63:3e:58) via eth1
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.96.114 via 128.252.97.254
#Aug  6 09:07:32 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.96.114 (f0:de:f1:63:3e:58) via eth1

import re
import sys
#import sqlite3
import datetime
import logging
import time
import os
import MySQLdb
import smtplib
import string
sys.path.append('/usr/local/etc/')
import dhcpcfg

# Read in global values from cofiguration file (dhcpcfg.py). 

#######################################################################
logFilePath = dhcpcfg.logFilePath                                     #
host = dhcpcfg.sqlHost                                                #
user = dhcpcfg.sqlUser                                                #
passwd = dhcpcfg.sqlPasswd                                            #
db = dhcpcfg.db							      #
senderEmail = dhcpcfg.senderEmail                                     #
senderPassword = dhcpcfg.senderPassword                               #
recipientEmails = dhcpcfg.recipientEmails                             #
#######################################################################


historyInsertions = 0
tempMacsInsertions = 0
clientsInsertions = 0

# The below three global variables are declared here to be used by the rest of the script. Year is referenced later on as needed, and todaysIDs is a list that populates with the primary key id's of mac addresses in the clients table of 'DBFilePath' who participated in a DHCPACK on the day infoblox.log.1 was constructed. At the end of the script, the table tempMacs is populated using the mac addresses from the clients table corresponding to the id's in 'todaysIDs'. 'TodaysHistories' will contain tuples of the form (<client primary keys>, <client's ip address>, <date-time string>) of entries already inserted into the history table today. Before an entry is inserted into the history table, todaysHistories is checked first, as to not add duplicate history entries. Furthermore, as to not waste memory, we keep todaysHistories <= 100 entries.

now = datetime.datetime.now()
yrstamp = datetime.datetime.now()  - datetime.timedelta(days = 1)
year = yrstamp.year
todaysIDs = []
todaysHistories = []

# This function opens the infoblox text log file at 'logFilePath'
def getLines(logFilePath):
	f = open(logFilePath)	
	return f

# This function uses the regular expression 'pattern' to find if the line passed to it from the infoblox log file describes a DHCPACK event. When a DHCPACK line is found, it matches the date, client's IP address, client's mac address, and client's hostname. It then passes this information to updateDB to update the database located at 'DBFilePath'
def processLine(line, conn, sqdb):
	pattern = re.compile('^(\w+\s+\d+\s+\d{2}:\d{2}:\d{2}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*(DHCPACK) on (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to (([0-9a-f]{2}[:-]){5}[0-9a-f]{2}) ?(?:\((.*)\))? via')
	match = pattern.match(line)
	if match:
		date = match.group(1)
		#dhcpServer = match.group(2)
		clientIP = match.group(4) #The clients ip address
		clientMA = match.group(5) #The clients mac address
		clientHN = None #The clients hostname (Only available sometimes)
		if match.group(7):
			clientHN = match.group(7) 
		updateDB(conn, sqdb, date, clientIP, clientMA, clientHN)

# This function is called when main() is called. If the script cannot find the tables it needs in the database specified by 'db' in the dhcpcfg.py config file, it creates them itself. Indexes are established on the clients and history tables for speed and efficeincy. The clients table contains only unique mac addresses. The history table contains records of each DHCPACK, with a foreign key reference to the associated client in the client's table. The tempMacs table contains mac addresses of recent DHCPACKS, and is purged once a week by the script '/usr/local/bin/rest.py'
def makeDB(db):
	try:
		db.execute('''CREATE TABLE clients (id INTEGER PRIMARY KEY AUTO_INCREMENT, macaddress CHAR(18) UNIQUE)''')
	except:
		print 'clients table already exists'
	try:
       		db.execute('''CREATE TABLE history (id INTEGER PRIMARY KEY AUTO_INCREMENT, clientid INTEGER, ip CHAR(30), date CHAR(30), clienthostname CHAR(40))''')
	except:
		print 'history table already exists'
	try:
		db.execute('''CREATE TABLE tempMacs (id INTEGER PRIMARY KEY AUTO_INCREMENT, macaddress CHAR(18) UNIQUE)''')
	except:
		print 'tempMacs table already exists'
	try:
		db.execute('''CREATE INDEX idx1 ON clients(macaddress)''')
	except:
		print ''
	try:
		db.execute('''CREATE INDEX idx2 ON history(clientid, date)''')
	except:
		print ''
        print '########## DATABASE INITIALIZED ##########'


# Given the information extracted by processLine() from an infoblox log line describing a DHCPACK, this function adds the appropriate information to the database.
def updateDB(conn, sqdb, date, clientIP, clientMA, clientHN):
	global todaysIDs
	global todaysHistories
	# Initialize clientID as None. clientID is the primary key of the primary key for the clients table. If a row is inserted into the clients, we change clientID to the correct primary key in the next else statement below.
	clientID = None

	#Special case for January 2nd when the variable 'year' is correct for entries corresponding to the 1st but not the 31st in the same infoblox.log.1 file
	if (now.month, now.day) == (1, 2) and date[0:6] == 'Dec 31':
		date = date + ' ' + str(year - 1)
	else:	
		#Get yesterdays year to supplement the date from the infoblox logs
		date = date + ' ' + str(year)

	# See if the mac address passed to us is already in the clients table. If it is not, insert it into the table. If not, do not insert it.
	sqdb.execute('SELECT id FROM clients WHERE macaddress = %s', (clientMA,))
	returnObject = sqdb.fetchone()
	lastRowId = sqdb.lastrowid
	if returnObject:
		logging.info('(db): Skipping macaddress: %s already found in database.', clientMA)
		clientID = returnObject[0]
	else:
		logging.info('(db): New mac address found, inserting %s into database.', clientMA)
		sqdb.execute('INSERT INTO clients VALUES (%s,%s)', [None, clientMA])
		lastRowId = sqdb.lastrowid
		clientID = int(conn.insert_id())
		global clientsInsertions
		clientsInsertions += 1
	#If clientID is not None and is not already in todaysIDs, append it to todaysIDs
	if clientID and clientID not in todaysIDs:
		todaysIDs.append(int(clientID))
		#print clientID


	#Do not add multiple rows in history for a user with identical times (date field). We do this because there are often duplicate lines in the infoblox.log.1 file that describe the same DHCPACK event at exactly the same time with the same user and information. This helps us from overpopulating the history table. If the clientID and date (timestamp from infoblox log file) already exist in the history table, it will be in todaysHistories, and we set 'exists' to 'True', and do not add a row to the history table. Otherwise, we check if the parameter 'clientHN' is 'None'. If it is not None, we add a row to the history table and append 'clientID' to 'todaysIDs' to be added to tempMacs.
	exists = False
	if ((clientID, clientIP, date) not in todaysHistories):
		todaysHistories.append((clientID, clientIP, date))
	else:
		exists = True
	#Update todaysHistories[] by deleting the first element (also the oldest element), so that it doesn't get too large and slow down the program.
	if len(todaysHistories) > 100:
		todaysHistories.pop(0)

	if exists is False:
		if clientHN != None:
			sqdb.execute('INSERT INTO history VALUES (%s,%s,%s,%s,%s)', [None, clientID, clientIP, date, clientHN])
			global historyInsertions
			historyInsertions += 1
		else:
			sqdb.execute('INSERT INTO history VALUES (%s,%s,%s,%s,NULL)', [None, clientID, clientIP, date])
			global historyInsertions
			historyInsertions += 1
	
	


#Builds tempMacs table using the primary key id's from the clients table that have been added to 'todaysIDs'. With this method, the tempMacs table will be updated each day with any new mac addresses that have participated in a DHCPACK in the last day. After the end of the week, the table will be used to update infoblox lease expiration dates by rest.py, which will also purge every value from tempMacs afterwards.
def buildTempMacs(sqdb):
	global todaysIDs
        for clientID in todaysIDs:
                sqdb.execute('SELECT macaddress FROM clients WHERE id = %s', (clientID,))
                ma = sqdb.fetchone()
		sqdb.execute('SELECT macaddress FROM tempMacs WHERE macaddress = %s', (ma[0],))
		returnObject = sqdb.fetchone()
		# If returnObject's type is not a tuple, it is None, and therefore is not in tempMacs and needs to be added
		if type(returnObject) is not tuple:
	                sqdb.execute('INSERT INTO tempMacs VALUES (%s,%s)', [None, ma[0]])
			global tempMacsInsertions
			tempMacsInsertions += 1
	

# The main function, runs each time the script is called
def main():

	startTime = time.time()
	# Open the log file at 'logFilePath' and return each line in an array called 'lines'. Also make iteration counter 'i' and line sum 'tot' to track script progress by percentage of lines parsed.
	lines = getLines(logFilePath)
	totlines = getLines(logFilePath)
	i = 0.0
	tot = sum(1 for l in totlines)
	
	conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
	conn.text_factory = str
	c = conn.cursor()
	makeDB(c)
	# Call processLine() on every line in 'lines'. processLine() calls updateDB(), so this iteration will update the database for every line from the infoblox log file describing a DHCPACK.
	for line in lines:
		processLine(line, conn, c)
		i = i + 1
		if i % 100000 == 0.0:
			print i / tot
	# Commit the changes to the database after the entire iteration is finished. This makes the script run hours faster than if commit() is called after each iteration.
	conn.commit()
	# Now that the list 'todaysIDs' has been constructed by the initial iteration, build the tempMacs table with buildTempMacs()
	buildTempMacs(c)
	# Commit to the database again now that the tempMacs table has been updated
	conn.commit()
	print 'DATABASE FULLY UPDATED'
	# Close the database connection
	conn.close()
	endTime = time.time()

	# Send out diagnostic emails
	
	msg = string.join(('From: Andrew Hannebrink', 'To: %s' % str(recipientEmails), 'Subject: Daily dhcplog.py Diagnostic Report', '', 'Total lines read in infoblox.log.1 = ' + str(i) + '\nhistory table insertions = ' + str(historyInsertions) + '\nclients table insertions = ' + str(clientsInsertions) + '\ntempMacs table insertions = ' + str(clientsInsertions) + '\ntotal time in seconds: ' + str(endTime - startTime)), '\r\n')
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(senderEmail, senderPassword)
	mail.sendmail(senderEmail, recipientEmails, msg)
	mail.close()
	
# Execute the main function
if __name__ == '__main__':
	sys.exit(main())
