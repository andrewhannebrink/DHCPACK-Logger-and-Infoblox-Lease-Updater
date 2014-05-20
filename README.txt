Andrew Hannebrink

	These are Python scripts for parsing infoblox DHCP log files, saving DHCPACK events into a bi-relational MySQL database, searching that database dynamically using a number of search parameter options, and automatically updating Infoblox DHCP lease expiration dates given the user's last DHCPACK event. This readme will provide a brief overview of the general workflow of the software, what each script does, and how to set up the automated system. For more detailed information on each method within each script, check the source code for the given script, as each file contains a large amount of step-by-step explanatory comments.


##############
#  WORKFLOW  #
##############

Three scripts and a MySQL database comprise this project: dhcplog.py, dhcpsearch.py, rest.py, and a MySQL database.

        ##########################################
	#  dhcplog.py and the 'dhcpdb' Database  #
	##########################################

	Saved at /usr/local/bin/dhcplog.py. This script runs once a day, parsing yesterday's Infoblox DHCP log file, loooking for lines describing a DHCPACK event. Then, it uploads this information to the database. When a DHCPACK event is found, it extracts the date, client's IP address, mac address, and hostname. Yesterday's Infoblox log file by default can be found at the path /var/log/infoblox.log.1. It can be very large, and for Washington University's network, is usually longer than five million lines on any given day. Below are five lines of a past log file, infoblox.log.1:

	#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.92.140 via 128.252.157.254
	#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.92.140 (00:1f:29:01:d5:72) via eth1
	#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: Hostname CC-036060 replaced by CC-036060
	#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPINFORM from 128.252.159.33 via 128.252.159.254
	#Aug  6 09:07:31 128.252.0.17 dhcpd[310]: DHCPACK to 128.252.159.33 (00:21:70:14:5d:79) via eth1

	This script conveniently groups all of the information to be loaded into the database with this regular expression:

	'^(\w+\s+\d+\s+\d{2}:\d{2}:\d{2}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .*(DHCPACK) on (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to (([0-9a-f]{2}[:-]){5}[0-9a-f]{2}) ?(?:\((.*)\))? via'
	Upon starting, the script also opens the database 'dhcpdb', looking for three tables: 'clients', 'history', and 'tempMacs'. If the script cannot find these tables, it executes queries for creating them. These three tables are formatted as follows:

	clients (
		id INTEGER PRIMARY KEY
		macaddress CHAR(18) UNIQUE
	);

	history (
		id INTEGER PRIMARY KEY
		clientid INTEGER (This is foreign key for id in the clients table)
		ip CHAR(30)		
		date CHAR(30)		
		clienthostname CHAR(40)
	);

	tempMacs (
		id INTEGER PRIMARY KEY
		macaddress CHAR(18) UNIQUE
	);



	The clients table keeps track of each unique hostname to receive a DHCPACK event in recent history. The history table keeps track of each unique DHCPACK event in recent history. Each row in the history table corresponds to a client from the clients table. The tempMacs table keeps track of all clients who have had a DHCPACK event in the last week. tempMacs is used once a week to update the DHCP leases of recent users. This table is also purged once a week by the rest.py script.

	###################
	#  dhcpsearch.py  #
	###################

	This script can be used for searching the database 'dhcpdb' from the command line, and should be saved at the path /usr/local/bin/dhcpsearch.py. For usage, run '$ python /usr/local/bin/dhcpsearch.py -h'. This command returns the following usage message:

	Search with three arguments.

The -p option specifies ip address. The ip address should be surrounded by quote ticks.

The -t option specifies the date and time, in the format: <'YYYY-MM-DD HH:MM:SS.00'> (military time surrounded by quote ticks).

The -i option specifies the time increment (in minutes) of how long of an increment you want to search over. The time increment should not be surrounded by quote ticks.

	#############
	#  rest.py  #
	#############	

	rest.py uses Infoblox's Python NIOS REST API to update users' lease expiration date within the Infoblox system by requesting and modifying JSON data objects for each user. rest.py runs once a week and should be saved at /usr/local/bin/rest.py. This script takes every entry from the tempMacs table in the 'dhcpdb' database, and attempts to update their DHCP lease expiration date to 180 days from the current date.

	IMPORTANT: In order for rest.py to run at decent pace, it needs to make a lot of concurrent HTTP 'GET' requests. So make sure that the Infoblox Grid Manager client has its http connection limit set to a high enough value with the command: '$ set connection_limit https <limit number', where <limit number> is between 0 and 2147483647, where 0 denotes no limit. This is also mentioned in the SET UP section of this read me.

	When this script finishes running, it clears the tempMacs table, preparing it to re-populate with next week's clients who participate in DHCPACKS.

	##################
	#  dhcppurge.py  #
	##################
	
	dhcppurge.py runs once a month, deleting rows from the history table that are a certain number of months old. So if it's May, and dbExpirationMonths is set to 2, all entries from March will be deleted, regardless of when the script runs in May.

	Next, dhcppurge.py removes any rows from the clients table that no longer have any corresponding entries in the history table.


	############
	#  SET UP  #
	############

	To set up this system, start by saving the files to the folling paths:
	
	/usr/local/bin/dhcplog.py
	/usr/local/bin/dhcpsearch.py
	/usr/local/bin/dhcppurge.py
	/usr/local/bin/rest.py
	/usr/local/etc/dhcpcfg.py

	Next, set up a Cron job. I created a new user with the ability to execute all six files, and set up their crontab file to look like this:
	
	# m h  dom mon dow   command
	00 03  *   *   *  python /usr/local/bin/dhcplog.py
	00 06  *   *   6  python /usr/local/bin/rest.py
	00 17  19  *   *  python /usr/local/bin/dhcppurge.py

	This runs dhcplog.py once a day at three in the morning, rest.py once a week on Saturday at six in the morning, and dhcppurge.py once a month on the nineteenth at five in the afternoon. 

	Next, edit the file /usr/local/etc/dhcpcfg.py to configure the program settings. This is what each variable means in dhcpcfg.py:

	logFilePath -	Path to infoblox DHCP log file, usually 'infoblox.log.1'

	sqlHost -	MySQL host, usually 'localhost'

	sqlUser -	Username of user to sign into MySQL with. Make sure that this user has permission to edit the database specified by the 'db' parameter below.

	sqlPasswd -	The MySQL user's corresponding MySQL password

	db -		Name of the MySQL database to be used. The software system can create the database structure and schema on its own, but you do need to make a database by this name manually. Though, there is no table creation necessary.
	
	senderEmail -	The email address used to send diagnostic reports of dhcplog.py, dhcppurge.py, and rest.py
	
	senderPassword -	senderEmail's password
	
	recipientEmails -	A python list of email addresses to send the diagnostic reports to
	
	maxLease -	The number of days used to set a user's DHCP expiration date into the future from their last DHCPACK event.

	infobloxUser -	The username for the Infoblox account used to connect to the Grid Master

	infobloxPasswd -	infobloxUser's password
	
	dbExpirationMonths -	Approximately the number of months to keep a history record before deleting it from the database. Check the section 'dhcppurge.py' in this README to see exactly how this works.
