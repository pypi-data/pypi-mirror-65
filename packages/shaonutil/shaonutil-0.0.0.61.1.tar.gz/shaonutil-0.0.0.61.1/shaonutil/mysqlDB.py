"""Mysql Database"""
from tkinter import ttk,Tk,Label,Entry
import tkinter as tk
from shaonutil.strings import generateCryptographicallySecureRandomString
import mysql.connector as mysql
import subprocess
import shaonutil
import os
import pandas

class MySQL:
	"""A class for all mysql actions"""
	def __init__(self,config,init_start_server=True,log=False):
		self.log = log
		self.init_start_server = init_start_server
		self.config = config

	def start_mysql_server(self):
		"""Start mysql server"""
		# --defaults-file=my.ini ->  mysql_config_file
		# instead
		# --port
		
		# --console If you omit the --console option, the server writes diagnostic output to the error log in the data directory
		# --log-error = error file
		# --debug - mysqld writes a log file C:\mysqld.trace that should contain the reason why mysqld doesn't start

		mysql_bin_folder = self._config['mysql_bin_folder']

		DETACHED_PROCESS = 0x00000008
		pids = shaonutil.process.is_process_exist('mysqld.exe')
		if not pids:
			#process = subprocess.Popen([os.path.join(mysql_bin_folder,"mysqld.exe"),"--defaults-file="+mysql_config_file,"--standalone","--debug"],creationflags=DETACHED_PROCESS)
			process = subprocess.Popen([os.path.join(mysql_bin_folder,"mysqld.exe"),"--standalone","--debug"],creationflags=DETACHED_PROCESS)
			print("Starting mysql server at pid",process.pid)
			return process
		else:
			print("MYSQL Server is already running at pids",pids)

	def stop_mysql_server(self,force=False):
		"""Stop MySQL Server"""
		# mysql_config_file
		mysql_bin_folder = self._config['mysql_bin_folder']
		user = self._config['user']
		password = self._config['password']

		pids = shaonutil.process.is_process_exist('mysqld.exe')
		if pids:
			print("MYSQL running at pids",pids)
			if force == True:
				shaonutil.process.killProcess_ByAll("mysqld.exe")
				print("Forced stop MySQL Server ...")
			else:
				DETACHED_PROCESS = 0x00000008	
				#mysqladmin -u robist_shaon --password=sh170892  shutdown
				process = subprocess.Popen([os.path.join(mysql_bin_folder,"mysqladmin.exe"),"-u",user,"--password="+password,"shutdown"]) # ,creationflags=DETACHED_PROCESS
				print("Stopping MySQL Server ...")
		else:
			print("MYSQL Server is not already running... , you can not close.")

	def reopen_connection(self):
		"""reopen"""
		print("MySQL > Explicitly opening connection ...")
		self.make_cursor()

	def close_connection(self):
		"""closing the connection"""
		print("MySQL > Explicitly closing connection ...")
		self._cursor.close()
		self.mySQLConnection.close()

	@property
	def config(self):
		return self._config
		
	@config.setter
	def config(self, new_value):
		self._config = new_value
		self.filter_config()
		self.make_cursor()
	
	def filter_config(self):
		mustList = ['host','user','password']
		for key in self._config:
			if not key in mustList:
				ValueError(key,"should have in passed configuration")
				break

	def make_cursor(self):
		if self.init_start_server:
			self.start_mysql_server()

		try:
			# Connection parameters and access credentials
			if 'database' in self._config:
				mySQLConnection = mysql.connect(
					host = self._config['host'],
					user = self._config['user'],
					passwd = self._config['password'],
					database = self._config['database']
				)
			else:
				mySQLConnection = mysql.connect(
					host = self._config['host'],
					user = self._config['user'],
					passwd = self._config['password']
				)
			self.mySQLConnection = mySQLConnection

		except mysql.errors.OperationalError:
			print("Error")
			# shaonutil.process.remove_aria_log('C:\\xampp\\mysql\\data')

		self._cursor = mySQLConnection.cursor()

	def is_mysql_user_exist(self,mysql_username):
		"""check if mysql user exist return type:boolean"""
		mySQLCursor = self._cursor
		mySqlListUsers = "select host, user from mysql.user;"
		mySQLCursor.execute(mySqlListUsers)
		userList = mySQLCursor.fetchall()
		foundUser = [user_ for host_,user_ in userList if user_ == mysql_username]
		if len(foundUser) == 0:
			return False
		else:
			return True

	def listMySQLUsers(self):
		"""list all mysql users"""
		cursor = self._cursor
		mySqlListUsers = "SELECT Host,User FROM MYSQL.USER"
		cursor.execute(mySqlListUsers)
		rows = cursor.fetchall()
		print("MySQL > Listing MySQL Users ...")
		
		data = {
			'Host' : [],
			'User' : [],
		}
		
		for row in rows:
			data = { key:data[key] + [row[list(data).index(key)]] for key in data}
		
		dbf = pandas.DataFrame(data)
		print(dbf)


	def createMySQLUser(self, host, userName, password,
	               querynum=0, 
	               updatenum=0, 
	               connection_num=0):
		"""Create a Mysql User"""
		cursor = self._cursor
		try:
			print("MySQL > Creating user",userName)
			sqlCreateUser = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';"%(userName,host,password)
			cursor.execute(sqlCreateUser)
		except Exception as Ex:
			print("Error creating MySQL User: %s"%(Ex));

	def delete_mysql_user(self,user,host,password=''):
		"""Delete a mysql user"""
		# drop by verifying by password convert password mysql password hash
		cursor = self._cursor
		query = f"""DROP USER '{user}'@'{host}'"""
		try:
			cursor.execute(query)
		except Exception as Ex:
			print("Error Deleting MySQL User: %s"%(Ex));


	def show_privileges(self,user,host):
		"""Show privileges of mysql user"""
		cursor = self._cursor
		
		try:
			print("MySQL > Showing privilages of user",user)
			query = f"""show grants for '{user}'@'{host}';"""
			cursor.execute(query)
			lines = cursor.fetchall()
			for line in lines:
				print(line)

		except Exception as Ex:
			print("Error showing privileges MySQL User: %s"%(Ex));

	def check_privileges(self,database,host,username):
		"""Check if a mysql user has privileges on a database"""
		pass

	def grant_all_privileges(self, host, userName,
				privileges = "ALL PRIVILEGES",
				database = '*',
				table = '*',
	            querynum=0, 
	            updatenum=0,
	            connection_num=0):
		"""Grant a user all privilages"""
		cursor = self._cursor
		
		try:
			print("MySQL > Granting all PRIVILEGES to user",userName)
			query = f"""GRANT {privileges} ON {database}.{table} TO '{userName}'@'{host}'"""
			print(query)
			cursor.execute(query)
			self.flush_privileges()

		except Exception as Ex:
			print("Error creating MySQL User: %s"%(Ex));

	def grant_privileges(self,user,host,database,privileges,table='*'):
		"""Grant specified privileges for a mysql user"""
		#SELECT,INSERT,UPDATE,DELETE
		cursor = self._cursor
		try:
			print("MySQL > Granting privilages",privileges,"for user",user)
			query = f"""GRANT {privileges} ON `{database}`.{table} TO '{user}'@'{host}';"""
			#GRANT ALL privileges ON `bookrack`.* TO 'robist_shaon'@'localhost'
			cursor.execute(query)
			lines = cursor.fetchall()
			for line in lines:
				print(line)

		except Exception as Ex:
			print("Error granting privileges MySQL User: %s"%(Ex));

	def remove_all_privileges(self,user,host,privileges = "all privileges"):
		"""Revoke/Remove all privileges for a mysql user"""
		cursor = self._cursor
		
		try:
			print("MySQL > Removing all privilages for user",user)
			query=f"""revoke {privileges} on *.* from '{user}'@'{host}';"""
			cursor.execute(query)
			lines = cursor.fetchall()
			for line in lines:
				print(line)

		except Exception as Ex:
			print("Error removing privileges MySQL User: %s"%(Ex));

	def remove_privileges(self,user,host,privileges):
		"""Remove specified privileges for a mysql user"""
		#SELECT,INSERT,UPDATE,DELETE
		try:
			print("MySQL > Removing privilages",privileges,"for user",user)
			query = f"""REVOKE {privileges} ON *.* FROM '{user}'@'{host}'"""
			#query = f"""REVOKE {privileges} ON `bookrack`.* FROM '{user}'@'{host}'"""
			#query = f"""REVOKE {privileges} ON `bookrack`.`tbname` FROM '{user}'@'{host}'"""

			cursor.execute(query)
			lines = cursor.fetchall()
			for line in lines:
				print(line)

		except Exception as Ex:
			print("Error granting privileges MySQL User: %s"%(Ex));
	

	def change_privileges(self,user,host,privileges):
		"""Change to specified privileges for a mysql user"""
		self.remove_privileges(user,host)
		self.grant_privileges(user,host,privileges)
		self.flush_privileges()


	def flush_privileges(self):
		"""Update database permissions/privilages"""
		cursor = self._cursor
		print("MySQL > Flushing privilages ...")
		cursor.execute("FLUSH PRIVILEGES;")

	def add_db_privilages_for_MySQLUSer(self):
		#Switch to mysql db.Give user privilages for a db.
		#INSERT INTO [table name] (Host,Db,User,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv) VALUES ('%','db','user','Y','Y','Y','Y','Y','N');
		pass

	def change_db_privilages_for_MySQLUSer(self):
		pass

	

	def is_db_exist(self,dbname):
		"""Check if database exist"""
		databases = self.get_databases()
		if dbname not in databases:
			return False
		else:
			return True

	def create_database(self,dbname):
		"""Create Database"""
		cursor = self._cursor
		print("MySQL > Creating database "+dbname+" ...")
		cursor.execute("CREATE DATABASE "+dbname)

	def delete_database(self,dbname):
		"""Delete Database"""
		cursor = self._cursor
		tables = self.get_tables()
		for table in tables:
			self.delete_table(table,dbname)

		print("MySQL > Deleting database "+dbname+" ...")
		cursor.execute("DROP DATABASE "+dbname)

	def get_databases(self):
		"""Get databases names"""
		cursor = self._cursor
		#print("MySQL > Getting databases ...")
		cursor.execute("SHOW DATABASES ")
		databases = cursor.fetchall()
		databases = [ x[0] for x in databases ]
		return databases

	

	def create_table(self,tbname,column_info):
		"""Create a table under a database"""
		cursor = self._cursor
		print("MySQL > Creating table "+tbname+" ...")
		cursor.execute("CREATE TABLE "+tbname+" (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"+''.join([' '+info+' '+column_info[info]+',' for info in column_info])[:-1]+")")

	def delete_table(self,table,database=''):
		"""Delete a table under a database"""
		cursor = self._cursor
		if database == '':
			database = self._config['database']
		print("MySQL > Deleting table "+table+" ...")
		query = f"""DROP TABLE {database}.{table}"""
		cursor.execute(query)

	def get_tables(self,database=''):
		"""Get table names"""
		cursor = self._cursor
		if database == '':
			database = self._config['database']
		cursor.execute(f"""SHOW TABLES FROM {database}""")
		tables = cursor.fetchall()
		tables = [ x[0] for x in tables ]
		return tables

	def describe_table(self,tbname):
		"""Describe a table structure"""
		"""
		Similars
		SHOW COLUMNS FROM bookrack.books;
		DESCRIBE bookrack.books;
		DESC bookrack.books;
		"""
		cursor = self._cursor
		print("MySQL > Describing table "+tbname+" ...")
		query = f"""DESCRIBE {tbname}"""
		cursor.execute(query)
		rows = cursor.fetchall()
		
		data = {
			'Field' : [],
			'Type' : [],
			'Null' : [],
			'Key' : [],
			'Default': [],
			'Extra' : []
		}

		for row in rows:
			data = { key:data[key] + [row[list(data).index(key)]] for key in data}
		
		dbf = pandas.DataFrame(data)
		print(dbf)

	def is_table_exist(self,tbname):
		"""Check if table exist"""
		tables = self.get_tables()
		if tbname in tables:
			return True
		else:
			return False

	def get_columns(self,tbname):
		"""Get column names of a table"""
		cursor = self._cursor
		cursor.execute("SHOW COLUMNS FROM "+tbname)
		columns = cursor.fetchall()
		return [column_name for column_name, *_ in columns]

	def update_row(self):
		#To update info already in a table.
		#UPDATE [table name] SET Select_priv = 'Y',Insert_priv = 'Y',Update_priv = 'Y' where [field name] = 'user';
		pass
	def delete_row():
		#Delete a row(s) from a table.
		#DELETE from [table name] where [field name] = 'whatever';
		pass

	def add_column(self,tbname,column_name):
		#Add a new column to db.
		#alter table [table name] add column [new column name] varchar (20);
		pass

	def delete_column(self,tbname,column_name):
		#Delete a column.
		#alter table [table name] drop column [column name];
		pass

	def delete_unique_column(self,tbname,column_name):
		#Delete unique column from table.
		#alter table [table name] drop index [colmn name];
		pass

	def change_to_unique_column(self):
		#Make a unique column so you get no dupes.
		#alter table [table name] add unique ([column name]);
		pass

	def change_column(self):
		#Make a column bigger.
		#alter table [table name] modify [column name] VARCHAR(3);
		pass


	def rename_column(self,tbname,old_column_name,new_column_name):
		# RENAME or Change Column name Structure
		#alter table [table name] change [old column name] [new column name] varchar (50);
		pass

	def backup_all(self):
		#Dump all databases for backup. Backup file is sql commands to recreate all db's.
		#mysql dir]/bin/mysqldump -u root -ppassword --opt >/tmp/alldatabases.sql
		pass
	def backup_table(self):
		#Dump a table from a database.
		#[mysql dir]/bin/mysqldump -c -u username -ppassword databasename tablename > /tmp/databasename.tablename.sql
		pass
	def backup_database(self):
		#Dump one database for backup.
		#[mysql dir]/bin/mysqldump -u username -ppassword --databases databasename >/tmp/databasename.sql
		pass
	def restore_table(self):
		#Restore database (or database table) from backup.
		#[mysql dir]/bin/mysql -u username -ppassword databasename < /tmp/databasename.sql
		pass
	def restore_databalse(self):
		#Restore database (or database table) from backup.
		#[mysql dir]/bin/mysql -u username -ppassword databasename < /tmp/databasename.sql
		pass

	def load_CSV_into_table(self):
		#Load a CSV file into a table.
		#LOAD DATA INFILE '/tmp/filename.csv' replace INTO TABLE [table name] FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (field1,field2,field3);
		pass


	def show_table(self,tbname):
		cursor = self._cursor
		print("MySQL > Showing data of table "+tbname+" ...")
		cursor.execute("SELECT * FROM "+tbname)
		rows = cursor.fetchall()

		data = { column_name:[] for column_name in self.get_columns(tbname)}
		for row in rows:
			data = { key:data[key] + [row[list(data).index(key)]] for key in data}
		
		dbf = pandas.DataFrame(data)
		print(dbf)



	def get_unique_id_from_field(self,field_name,key_length,filters=[]):
		"""Get a random unique id not registered in a specific field"""
		table = self._config['table']

		cursor = self._cursor

		sid = generateCryptographicallySecureRandomString(stringLength=key_length,filters=filters)
		
		
		while True:
			query = "SELECT * FROM "+table+" WHERE `"+field_name+"` = '"+sid+"'"

			## getting records from the table
			cursor.execute(query)

			## fetching all records from the 'cursor' object
			records = cursor.fetchall()

			## Showing the data
			for record in records:
			    print(record)


			if(len(records)>1):
				print("matched with previously stored sid")
				sid = generateCryptographicallySecureRandomString(stringLength=key_length,filters=filters)
			else:
				print("Got unique sid")
				break
				
		return sid

	def delete_row(self,delete_dict):
		"""Delete a row of data"""
		#keylist = [key for key in delete_dict]
		column_name = delete_dict[0]
		value = delete_dict[column_name]

		cursor = self._cursor
		tbname = self._config['table']
		query = f"""DELETE FROM {tbname} WHERE `{column_name}`='{value}';"""
		cursor.execute(query)

		## to make final output we have to run the 'commit()' method of the database object
		#self.mySQLConnection.commit()

		#print(cursor.rowcount, "record inserted")

	def insert_row(self,value_tupple):
		"""Insert row of data"""
		cursor = self._cursor
		dbname = self._config['database']
		tbname = self._config['table']
		column_info = self.get_columns(tbname)[1:]
		
		# candidate_name, candidate_age, candidate_distance, candidate_living_place, candidate_university_or_instituition, candidate_image_webp_url, candidate_unique_image_name
		#cursor.execute("DESC "+tbname)


		query = "INSERT INTO "+tbname+ ' (' + ''.join([key+', ' for key in column_info])[:-2] + ') VALUES ('+ ''.join(['%s, ' for key in column_info])[:-2]  +')'
		
		## storing values in a variable
		values = [
		    value_tupple
		]

		## executing the query with values
		cursor.executemany(query, values)

		## to make final output we have to run the 'commit()' method of the database object
		self.mySQLConnection.commit()

		print(cursor.rowcount, "record inserted")

def create_configuration(option='cli',file_name = "private/config.ini"):
	"""Creating Configuration"""
	if option == 'cli':
		print('Getting your configurations to save it.\n')
		print('\nDatabase configurations -')
		dbhost = input('Give your db host : ')
		dbuser = input('Give your db user : ')
		dbpassword = input('Give your db password : ')
		dbname = input('Give your db name : ')
		dbtable = input('Give your db table : ')

		mysql_bin_folder = input('Give your path of mysql bin folder : ')

		configstr = f"""; config file
[DB_INITIALIZE]
mysql_bin_folder = {mysql_bin_folder}
host = localhost
user = root
password = 
[DB_AUTHENTICATION]
mysql_bin_folder = {mysql_bin_folder}
host = {dbhost}
user = {dbuser}
password = {dbpassword}
database = {dbname}
table = {dbtable}
[MYSQL]
mysql_bin_folder = {mysql_bin_folder}"""

		shaonutil.file.write_file(file_name,configstr)

	elif option == 'gui':
		window = Tk()
		window.title("Welcome to DB Config")
		window.geometry('400x400')
		window.configure(background = "grey");

		# Label fb_authentication
		FB_LABEL = Label(window ,text = "MYSQL Config").grid(row = 0,column = 0,columnspan=2)
		a = Label(window ,text = "MYSQL bin folder").grid(row = 1,column = 0)
		
		DB_LABEL = Label(window ,text = "Database Authentication").grid(row = 3,column = 0,columnspan=2)
		c = Label(window ,text = "Host").grid(row = 4,column = 0)
		d = Label(window ,text = "User").grid(row = 5,column = 0)
		d = Label(window ,text = "Password").grid(row = 6,column = 0)
		d = Label(window ,text = "Database").grid(row = 7,column = 0)
		d = Label(window ,text = "Table").grid(row = 8,column = 0)

		mysqlbinfolder_ = tk.StringVar(window)
		fbpassword_ = tk.StringVar(window)
		dbhost_ = tk.StringVar(window)
		dbuser_ = tk.StringVar(window)
		dbpassword_ = tk.StringVar(window)
		dbname_ = tk.StringVar(window)
		dbtable_ = tk.StringVar(window)

		Entry(window,textvariable=mysqlbinfolder_).grid(row = 1,column = 1)
		
		Entry(window,textvariable=dbhost_).grid(row = 4,column = 1)
		Entry(window,textvariable=dbuser_).grid(row = 5,column = 1)
		Entry(window,show="*",textvariable=dbpassword_).grid(row = 6,column = 1)
		Entry(window,textvariable=dbname_).grid(row = 7,column = 1)
		Entry(window,textvariable=dbtable_).grid(row = 8,column = 1)

		def clicked():
			mysql_bin_folder = mysqlbinfolder_.get()
			
			dbhost = dbhost_.get()
			dbuser = dbuser_.get()
			dbpassword = dbpassword_.get()
			dbname = dbname_.get()
			dbtable = dbtable_.get()

			configstr = f"""; config file
[DB_INITIALIZE]
mysql_bin_folder = {mysql_bin_folder}
host = localhost
user = root
password = 
[DB_AUTHENTICATION]
mysql_bin_folder = {mysql_bin_folder}
host = {dbhost}
user = {dbuser}
password = {dbpassword}
database = {dbname}
table = {dbtable}
[MYSQL]
mysql_bin_folder = {mysql_bin_folder}"""

			shaonutil.file.write_file(file_name,configstr)

			window.destroy()


		btn = ttk.Button(window ,text="Submit",command=clicked).grid(row=9,column=0)
		window.mainloop()


def remove_aria_log(mysql_data_dir):
	"""Removing aria_log.### files to in mysql data dir to restart mysql"""
	aria_log_files = [file for file in os.listdir(mysql_data_dir) if 'aria_log.' in file]

	for aria_log in aria_log_files:
		aria_log = os.path.join(mysql_data_dir,aria_log)
		os.remove(aria_log)

def get_mysql_datadir(mysql_bin_folder,user,pass_=''):
	"""Get mysql data directory"""
	process = subprocess.Popen([os.path.join(mysql_bin_folder,"mysql"),"--user="+user,"--password="+pass_,"-e","select @@datadir;"],stdout=subprocess.PIPE)
	out, err = process.communicate()
	out = [line for line in out.decode('utf8').replace("\r\n","\n").split('\n') if line != ''][-1]
	datadir = out.replace('\\\\','\\')
	return datadir

"""
To login (from unix shell) use -h only if needed.	[mysql dir]/bin/mysql -h hostname -u root -p
Create a database on the sql server.	create database [databasename];
List all databases on the sql server.	show databases;
Switch to a database.	use [db name];
To see all the tables in the db.	show tables;
To see database's field formats.	describe [table name];
To delete a db.	drop database [database name];
To delete a table.	drop table [table name];
Show all data in a table.	SELECT * FROM [table name];
Returns the columns and column information pertaining to the designated table.	show columns from [table name];	
Show certain selected rows with the value "whatever".	SELECT * FROM [table name] WHERE [field name] = "whatever";	
Show all records containing the name "Bob" AND the phone number '3444444'.	SELECT * FROM [table name] WHERE name = "Bob" AND phone_number = '3444444';	
Show all records not containing the name "Bob" AND the phone number '3444444' order by the phone_number field.	SELECT * FROM [table name] WHERE name != "Bob" AND phone_number = '3444444' order by phone_number;	
Show all records starting with the letters 'bob' AND the phone number '3444444'.	SELECT * FROM [table name] WHERE name like "Bob%" AND phone_number = '3444444';	
Use a regular expression to find records. Use "REGEXP BINARY" to force case-sensitivity. This finds any record beginning with a.	SELECT * FROM [table name] WHERE rec RLIKE "^a$";	
Show unique records.	SELECT DISTINCT [column name] FROM [table name];
Show selected records sorted in an ascending (asc) or descending (desc).	SELECT [col1],[col2] FROM [table name] ORDER BY [col2] DESC;
Count rows.	SELECT COUNT(*) FROM [table name];	
Join tables on common columns.	select lookup.illustrationid, lookup.personid,person.birthday from lookup
left join person on lookup.personid=person.personid=statement to join birthday in person table with primary illustration id;
Change a users password.(from unix shell).	[mysql dir]/bin/mysqladmin -u root -h hostname.blah.org -p password 'new-password'
Change a users password.(from MySQL prompt).	SET PASSWORD FOR 'user'@'hostname' = PASSWORD('passwordhere');
Switch to mysql db.Give user privilages for a db.	INSERT INTO [table name] (Host,Db,User,Select_priv,Insert_priv,Update_priv,Delete_priv,Create_priv,Drop_priv) VALUES ('%','db','user','Y','Y','Y','Y','Y','N');


Create Table Example 1.	CREATE TABLE [table name] (firstname VARCHAR(20), middleinitial VARCHAR(3), lastname VARCHAR(35),suffix VARCHAR(3),
officeid VARCHAR(10),userid VARCHAR(15),username VARCHAR(8),email VARCHAR(35),phone VARCHAR(25), groups
VARCHAR(15),datestamp DATE,timestamp time,pgpemail VARCHAR(255));
Create Table Example 2.	create table [table name] (personid int(50) not null auto_increment primary key,firstname varchar(35),middlename varchar(50),lastname varchar(50) default 'bato');
"""



"""
Summary of Available Privileges
The following table shows the static privilege names used in GRANT and REVOKE statements, along with the column name associated with each privilege in the grant tables and the context in which the privilege applies.

Table 6.2 Permissible Static Privileges for GRANT and REVOKE

Privilege	Grant Table Column	Context
ALL [PRIVILEGES]	Synonym for “all privileges”	Server administration
ALTER	Alter_priv	Tables
ALTER ROUTINE	Alter_routine_priv	Stored routines
CREATE	Create_priv	Databases, tables, or indexes
CREATE ROLE	Create_role_priv	Server administration
CREATE ROUTINE	Create_routine_priv	Stored routines
CREATE TABLESPACE	Create_tablespace_priv	Server administration
CREATE TEMPORARY TABLES	Create_tmp_table_priv	Tables
CREATE USER	Create_user_priv	Server administration
CREATE VIEW	Create_view_priv	Views
DELETE	Delete_priv	Tables
DROP	Drop_priv	Databases, tables, or views
DROP ROLE	Drop_role_priv	Server administration
EVENT	Event_priv	Databases
EXECUTE	Execute_priv	Stored routines
FILE	File_priv	File access on server host
GRANT OPTION	Grant_priv	Databases, tables, or stored routines
INDEX	Index_priv	Tables
INSERT	Insert_priv	Tables or columns
LOCK TABLES	Lock_tables_priv	Databases
PROCESS	Process_priv	Server administration
PROXY	See proxies_priv table	Server administration
REFERENCES	References_priv	Databases or tables
RELOAD	Reload_priv	Server administration
REPLICATION CLIENT	Repl_client_priv	Server administration
REPLICATION SLAVE	Repl_slave_priv	Server administration
SELECT	Select_priv	Tables or columns
SHOW DATABASES	Show_db_priv	Server administration
SHOW VIEW	Show_view_priv	Views
SHUTDOWN	Shutdown_priv	Server administration
SUPER	Super_priv	Server administration
TRIGGER	Trigger_priv	Tables
UPDATE	Update_priv	Tables or columns
USAGE	Synonym for “no privileges”	Server administration

The following table shows the dynamic privilege names used in GRANT and REVOKE statements, along with the context in which the privilege applies.


Table 6.3 Permissible Dynamic Privileges for GRANT and REVOKE

Privilege	Context
APPLICATION_PASSWORD_ADMIN	Dual password administration
AUDIT_ADMIN	Audit log administration
BACKUP_ADMIN	Backup administration
BINLOG_ADMIN	Backup and Replication administration
BINLOG_ENCRYPTION_ADMIN	Backup and Replication administration
CLONE_ADMIN	Clone administration
CONNECTION_ADMIN	Server administration
ENCRYPTION_KEY_ADMIN	Server administration
FIREWALL_ADMIN	Firewall administration
FIREWALL_USER	Firewall administration
GROUP_REPLICATION_ADMIN	Replication administration
INNODB_REDO_LOG_ARCHIVE	Redo log archiving administration
NDB_STORED_USER	NDB Cluster
PERSIST_RO_VARIABLES_ADMIN	Server administration
REPLICATION_APPLIER	PRIVILEGE_CHECKS_USER for a replication channel
REPLICATION_SLAVE_ADMIN	Replication administration
RESOURCE_GROUP_ADMIN	Resource group administration
RESOURCE_GROUP_USER	Resource group administration
ROLE_ADMIN	Server administration
SESSION_VARIABLES_ADMIN	Server administration
SET_USER_ID	Server administration
SHOW_ROUTINE	Server administration
SYSTEM_USER	Server administration
SYSTEM_VARIABLES_ADMIN	Server administration
TABLE_ENCRYPTION_ADMIN	Server administration
VERSION_TOKEN_ADMIN	Server administration
XA_RECOVER_ADMIN	Server administration

"""