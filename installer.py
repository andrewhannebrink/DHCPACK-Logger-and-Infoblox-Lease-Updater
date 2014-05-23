#!/usr/bin/python
#Andrew Hannebrink

#!! THIS SCRIPT IS STILL UNDER CONSTRUCTION

# This script installs the package files into the correct locations, creates a UNIX user named 'dhcplog', grants them permissions to the files, and sets up their crontab file for executing these files. It also sets up the MySQL database.

import sys
import os
import pexpect
import subprocess

unixUser = 'user'
unixPass = 'password'


def main():
	op = os.system('useradd -m ' + unixUser)
	#If user doesn't exist (exit code 0) , set their password
	if op == 0:
		p = pexpect.spawn('passwd ' + unixUser)
		p.expect('Enter new UNIX password: ')
		p.sendline(unixPass)
		p.expect('Retype new UNIX password: ')
		p.sendline(unixPass)
	#Copy files
	os.system('cp dhcpsearch.py /usr/local/bin/dhcpsearch.py')
	os.system('cp dhcplog.py /usr/local/bin/dhcplog.py')
	os.system('cp dhcpcfg.py /usr/local/bin/dhcpcfg.py')
	os.system('cp dhcppurge.py /usr/local/bin/dhcppurge.py')
	os.system('cp rest.py /usr/local/bin/rest.py')
	
	cron1 = '00 03  *   *   *  dhcplog python /usr/local/bin/dhcplog.py\n'
	cron2 = '00 06  *   *   6  dhcplog python /usr/local/bin/rest.py\n'
	cron3 = '00 17  19  *   *  dhcplog python /usr/local/bin/dhcppurge.py\n'
	if os.path.exists('/etc/cron.d/dhcplogcron'):
		a = ''
		while a != 'y' and a != 'n':
			a = raw_input('/etc/cron.d/dhcplogcron cron file already exists. Overwrite it? [y/n]')
		if a == 'y':
			print 'overwriting /etc/cron.d/dhcplogcron...'
			os.system('rm /etc/cron.d/dhcplogcron')
			
	f = open('/etc/cron.d/dhcplogcron','w+')
	f.write(cron1 + cron2 + cron3)
	f.close()

	

	

if __name__ == '__main__':
	sys.exit(main())
