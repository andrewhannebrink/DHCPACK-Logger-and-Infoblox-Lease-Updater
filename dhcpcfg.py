#!/usr/bin/python
#Andrew Hannebrink

#This is a configuration file written in Python source code for ease of manipulation. Save it at /usr/local/etc/dhcpcfg.py. This file is read when dhcplog.py, dhcpsearch.py, rest.py, and dhcppurge.py run. These parameters are necessary for the program to work, and may contain sensitive information, so it is suggested to make a user whose sole purpose is to own and execute files associated with this software system.

logFilePath = '/var/log/infoblox.log.1'
sqlHost = 'localhost'
sqlUser = '<PUT MYSQL USER HERE>'
sqlPasswd = '<PUT MYSQL USER\'S PASSWORD HERE>'
db = '<NAME OF DATABASE>'
senderEmail = '<EMAIL ADDRESS USED TO SEND DIAGNOSTIC REPORTS>'
senderPassword = '<PASSWORD FOR EMAIL ADDRESS USED TO SEND DIAGNOSTIC REPORTS>'
recipientEmails = ['DIAGNOSTIC REPORT RECIPIENT EMAIL ADDRESS \#1', '<DIAGNOSTIC REPORT RECIPIENT EMAIL ADDRESS \#2']
maxLease = 180 			# NUMBER OF DAYS FROM LAST DHCPACK TO SET USERS' DHCP LEASE EXPIRATION DATES
ibxUrl = 'INFOBLOX GRID MASTER URL' # i.e. 'https://gm.ip.wustl.edu/wapi/v1.2/'
infobloxUser = '<GRID MASTER LOGIN USERNAME>'
infobloxPasswd = '<GRID MASTER LOGIN PASSWORD>'
dbExpirationMonths = 6 		# MONTHS TO KEEP RECORDS IN HISTORY TABLE (DONT MAKE THIS LARGER THAN 11)

