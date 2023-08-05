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

	def grantMySQLUserAllPrivileges(self, host, userName,
	               querynum=0, 
	               updatenum=0, 
	               connection_num=0):
		"""Grant a user all privilages"""
		cursor = self._cursor
		try:
			print("MySQL > Granting all PRIVILEGES to user",userName)
			sqlGrantPrivilage = "GRANT ALL PRIVILEGES ON * . * TO '%s'@'%s';"%(userName,host)
			cursor.execute(sqlGrantPrivilage)
			cursor.execute("FLUSH PRIVILEGES;")

		except Exception as Ex:
			print("Error creating MySQL User: %s"%(Ex));

	def is_db_exist(self,dbname):
		"""Check if database exist"""
		databases = self.get_databases()
		if dbname not in databases:
			return False
		else:
			return True

	def create_db(self,dbname):
		"""Create Database"""
		cursor = self._cursor
		print("MySQL > Creating database "+dbname+" ...")
		cursor.execute("CREATE DATABASE "+dbname)

	def delete_db(self,dbname):
		"""Delete Database"""
		cursor = self._cursor
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

	def delete_table(self,tbname):
		"""Delete a table under a database"""
		cursor = self._cursor
		print("MySQL > Deleting table "+tbname+" ...")
		query = f"""DROP TABLE {tbname}"""
		cursor.execute(query)

	def get_tables(self):
		"""Get table names"""
		cursor = self._cursor
		cursor.execute('SHOW TABLES')
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
		column_info = self.get_columns_names(tbname)[1:]
		
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