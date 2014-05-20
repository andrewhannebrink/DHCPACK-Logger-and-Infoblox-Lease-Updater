#!/usr/bin/python
#Andrew Hannebrink

#This script is used for searching the database, 'dhcpdb'. Run '$ python /usr/local/bin/dhcpsearch.py -h for more information.

import sys
import getopt
import datetime
import dateutil.parser
import MySQLdb
sys.path.append('/usr/local/etc/')
import dhcpcfg

############################################################
host = dhcpcfg.sqlHost                                     #
user = dhcpcfg.sqlUser                                     #
passwd = dhcpcfg.sqlPasswd                                 #
db = dhcpcfg.db                                            #
############################################################

def main():
	helpBool = False
	searchMac = False
	searchClientHN = False
	searchTime = False
	searchIncrement = False
	searchIP = False
	
	conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
	conn.text_factory = str
	sqdb = conn.cursor()

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hm:c:t:i:p:')
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(-1)
	for opt, arg in opts:
		if opt == '-h':
			helpBool = True
		if (opt == '-m') & (arg != ''):
			searchMac = True
			macAddressArg = arg.lower()
		if (opt == '-c') & (arg != ''):
			searchClient = True
			clientArg = arg
		if (opt == '-t') & (arg != ''):
			searchTime = True
			timeArgStr = arg
		if (opt == '-i') & (arg != ''):
			searchIncrement = True
			incrementArg = arg
		if (opt == '-p') & (arg != ''):
			searchIP = True
			ipArg = arg
	
	if helpBool == True:
		print ''
		print 'Search with three arguments.'
		print ''
		print 'The -p option specifies ip address. The ip address should be surrounded by quote ticks.'
		print ''
		print 'The -t option specifies the date and time, in the format: <\'YYYY-MM-DD HH:MM:SS.00\'> (military time surrounded by quote ticks).'
		print ''
		print 'The -i option specifies the time increment (in minutes) of how long of an increment you want to search over. The time increment should not be surrounded by quote ticks.'
		print ''
		sys.exit(0)

	if (searchTime != True) | (searchIncrement != True):
		print 'Please search usings a start time with the "-t" option, and a time increment with the "-i" option. Use the "-h" option for more information.'
		sys.exit(0)
	
	hquery = 'SELECT * FROM history WHERE '

	print '#######################################################################################################'
	print 'IP Address: ' + ipArg
	print '#######################################################################################################'
	print 'Mac Address		Host Name		Time'
	print '-------------------------------------------------------------------------------------------------------'
	if searchIP is True:
		temp = 'ip = \'' + ipArg + '\''
		hquery = hquery + temp
		sqdb.execute(hquery)	
		historyGetter = sqdb.fetchall()
		prevID = 0
		macAddress = ''
		returnHistories = []
		timeArg = dateutil.parser.parse(timeArgStr)
		for histRow in historyGetter:
			timeStr = histRow[3]
			time = datetime.datetime.strptime(timeStr, '%b %d %H:%M:%S %Y')
			timeDelta = time - timeArg
			if (time > (timeArg-datetime.timedelta(minutes=int(incrementArg)))) & (time < (timeArg+datetime.timedelta(minutes=int(incrementArg)))):
				returnHistories.append(histRow)
		timeArg = dateutil.parser.parse(timeArgStr)
		for histRow in returnHistories:
			timeStr = histRow[3]
			time = datetime.datetime.strptime(timeStr, '%b %d %H:%M:%S %Y')
			timeDelta = time - timeArg
			clientID = histRow[1]
			if clientID != prevID:
				cquery = 'SELECT * FROM clients WHERE id = ' + str(clientID)
				sqdb.execute(cquery)
				macGetter = sqdb.fetchone()
				macAddress = macGetter[1]
			hostName = histRow[4]
			blankStr1 = '                        '
			blankStr2 = '                        '
			tempStr1 = macAddress + blankStr1[len(macAddress):]
			tempStr2 = hostName + blankStr2[len(hostName):]
			print tempStr1 + tempStr2 + str(time)	
			
if __name__ == '__main__':
	sys.exit(main())
