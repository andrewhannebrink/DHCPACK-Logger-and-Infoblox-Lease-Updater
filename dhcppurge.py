#!/usr/bin/python
#Andrew Hannebrink

#This script gets rid of rows in the history and clients tables that are older than the time limit (in months) specified a few lines down. The variable is called 'dbExpirationMonths'.

import datetime
import MySQLdb
import time
import string
import sys
import smtplib
sys.path.append('/usr/local/etc/')
import dhcpcfg

#########################################################################
dbExpirationMonths = dhcpcfg.dbExpirationMonths				# 
host = dhcpcfg.sqlHost							#
user = dhcpcfg.sqlUser							#
passwd = dhcpcfg.sqlPasswd						#
db = dhcpcfg.db								#
senderEmail = dhcpcfg.senderEmail					#
senderPassword = dhcpcfg.senderPassword					#
recipientEmails = dhcpcfg.recipientEmails				#
#########################################################################


def main():
	startTime = time.time()
	monthMap = { 1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec' }
	now = datetime.datetime.now()
	thenMonth = now.month - dbExpirationMonths
	#Adjust month for negative months
	while thenMonth < 1:
		thenMonth += 12
	conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
	conn.text_factory = str
	c = conn.cursor()
	print 'deleting entries...'
	c.execute('DELETE FROM history WHERE LEFT(date, 3) = %s', (monthMap[thenMonth],))
	# Delete any clients who no longer have any correponding entries in the history table
	c.execute('DELETE FROM clients WHERE id NOT IN (SELECT clientid FROM history)')
	conn.commit()
	conn.close()

	print 'finished deleting entries...'
	endTime = time.time()
	#Send diagnostic email
	txt = 'Deleted entries in history table for month of ' + monthMap[thenMonth] + ' in ' + str(endTime - startTime) + ' seconds.'
	msg = string.join(('From: Andrew Hannebrink', 'To: %s' % str(recipientEmails), 'Subject: Monthly dhcpPurge.py Diagnostic Report', '', txt), '\r\n')
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(senderEmail, senderPassword)
	mail.sendmail(senderEmail, recipientEmails, msg)
	mail.close

if __name__ == '__main__':
	sys.exit(main())
