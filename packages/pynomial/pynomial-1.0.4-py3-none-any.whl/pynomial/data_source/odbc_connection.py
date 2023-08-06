
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import pandas as pd
import pyodbc
import getpass
from ..pynomial_configuration import Configurations
import abc

class __MasterOdbc(object):

	"""
	
	This is the base/super class to manage connections based on ODBC drivers

	"""

	def __init__(self, quiet = False):
		self.__initialized = False
		self.quiet = quiet
		self.__drivers = []

		for driver in pyodbc.drivers():
			self.__drivers.append(driver)


	def _get_odbc_drivers(self):

		'''
		Gets the list of available ODBC drivers
		'''
		print ('The following drivers are provided: ')
		for driver in self.__drivers:
			print(str(driver))


	def check_driver(self, driver = None):
		'''
		This function is used to check if driver exists for a specific type of connection
		'''
		import re
		pattern = re.compile(driver)
		return [driver for driver in self.__drivers if pattern.search(driver)]

	@abc.abstractmethod
	def close(self):
		if not self.quiet:
			print('The connection is closed!')
		
	

class SqlServerConnection(__MasterOdbc):

	"""
	This is a class to facilitate connection to MS SQL server databases using Python implementation of ODBC (pyodbc).

	Parameters:
		server (str): Server name/address for connection
		database (str): Database name/initial catalog
		trusted_connection (bool): True if ``Windows Authentication`` is used
		uid (str) : User ID to login and access the server
		pwd (str) : Password

	An instance of this class contains server and database properties that can be set by the user which results in
	establishing a new connection to the new server/database. 

	Example:

		Quick connection into local server:

		.. code-block:: python
			import pynomial as pyn
			connection = pyn.ServerConnect(server='localhost',database='master', trusted_connection=True)

	"""
	def __str__(self):

		return 'An object to facilitate connection to a MS SQL server database'


	def __call__(self):

		print('Connection established to SQL Server')

		print('Server Name: {}'.format(self._server))
		self._get_server_version()
		print('Login information:')

		if self.trusted_connection:
			print('Trusted Connection')
			print('Initial Catalog: {}'.format(self._database))
		else:
			print('User Id: {}'.format(self.uid))
			print('Initial Catalog: {}'.format(self._database))

	# Context manager protocol (i.e. disposable object)
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()
		if isinstance(exc_value, ConnectionError):
			print('Connection Failed: Exception Type: {}, Exception Value: {}, Exception TraceBack: {}'.format(exc_type, exc_value, traceback))
		return

	def __init__(self, server = None, database = None, trusted_connection=False, uid = None, pwd = None, quiet=False, make_connection=True):

		'''
		Initialization of the class

		'''

		# Initialization inherited from the base class
		super().__init__(quiet=quiet)

		# Sanity check
		if server is None:
			raise ValueError('server Name is required!')

		if database is None:
			database = 'master'
			if not self.quiet:
				print('Database name was not provided (master was used)!')


		self._server = server
		self._database = database

		self.trusted_connection = trusted_connection

		# Initialize the connection
		if make_connection:
			self._make_connection(uid, pwd)
			self._initialized = True


	# Define properties
	#------------------
	# 1) Server
	def _getserver(self):
		return self._server

	def _setserver(self, value):

		if isinstance(value, str):
			self._server = value

			if self._initialized: # Establish a new connection if the server is changed
				self.uid = None
				self.pwd = None
				initial_catalog = getpass.getpass('Initial database/catalog : ')
				if initial_catalog is None:
					self._database = 'master'
				else:
					self._database = initial_catalog

		else:
			raise ValueError ('server entry must be string')

	server = property(_getserver, _setserver)

	# 2) Database
	def _getdatabase(self):
		return self._database

	def _setdatabase(self, value):
		if isinstance(value, str):
			self._database = value
			if self._initialized:
				self._make_connection(self.uid, self.pwd)
		else:
			raise ValueError ('database entry must be string')

	database = property(_getdatabase, _setdatabase)

	# 3) Server Version
	def _get_server_version(self):

		query ='''
		SELECT @@VERSION
		'''
		print(self.execute_query(query).values[0][0])

	server_version = property(_get_server_version)

	# 4) Drivers
	drivers = property(lambda self: self._get_odbc_drivers())

	
	
	def _make_connection_with_connection_string(self):
		try:
			self.connection = pyodbc.connect(self.connection_string)
		except Exception as e:
			raise ConnectionError('Failed to Connect to server\n'+str(e))


	def _make_connection(self, uid=None, pwd=None):

		'''
		Initializing connection to sql server
		'''

		# Sanity check
		if not self.trusted_connection:
			if uid is None:
				uid = input('User ID :')

			if pwd is None:
				pwd = getpass.getpass('Password for {}:'.format(uid))

			try:
				assert isinstance(uid,str)
				self.uid = uid
				assert isinstance(pwd,str)
				self.pwd = pwd
			except:
				raise ValueError ('user id/password entry must be string!')
		

		# check if the required ODBC drivers are installed and available
		sql_drivers = self.check_driver(driver = 'SQL Server')
		if len(sql_drivers) == 0:
			self._get_odbc_drivers()
			raise ValueError('Driver for SQL server was not found...')

		else:
			self.maindriver =  sql_drivers[0]


		if self.trusted_connection:

			connection_string = "DRIVER={%s};""server=%s;""Database=%s;""Trusted_Connection=yes"%(self.maindriver, self._server,self._database)

			try:
				self.connection = pyodbc.connect(connection_string)

			except Exception as e:

				raise ConnectionError('Failed to Connect to server\n'+str(e))
		else:

			connection_string = "DRIVER={%s};""server=%s;""Database=%s;""uid=%s;""pwd=%s"%(self.maindriver, self._server,self._database,self.uid,self.pwd)
			try:
				self.connection = pyodbc.connect(connection_string)
				connection_string = "DRIVER={%s};""server=%s;""Database=%s;""uid=%s;""pwd=%s"%(self.maindriver, self._server,self._database,self.uid,self.pwd)

			except Exception as e:

				raise ConnectionError('Failed to Connect to server\n'+ str(e))

		self.connection_string = connection_string

		if not self.quiet:
			print ('Successful Connection to {}'.format(self._server))

	def get_database_list(self ,system_db = False):

		'''
		A method to get the list of databases for a given connection

		'''

		if system_db:
			query = '''
			SELECT * FROM sys.databases
			'''
		else:
			query = '''
			SELECT * FROM sys.databases
			WHERE len(owner_sid)>1
			'''

		return self.execute_query(query)


	def execute_query (self,sql_query, **kwargs):

		"""
		This function is used to run a SQL query. It returns the resulting data as a pandas data frame

		Parameters:
			sql_query (str): the sql query that is passed to the assigned server and database to retrieve data

		Example:

			>>> df = connection.execute_query(sql_query)

		"""

		return pd.io.sql.read_sql(sql_query,self.connection, **kwargs)


	def deploy(self, command, **kwargs):

		'''
		This function can be used to deploy and commit a sql command into the target sql server using the inital catalog
		that is set during the initialization of PyEDW.ServerConnect

		Parameters:
			command (str): the command that is passed to the assigned server and database

		Example:

			>>> df = connection.deploy(command)

		'''
		try:
			with self.connection.cursor(**kwargs) as cursor: 
				cursor.execute(command, **kwargs)
				self.connection.commit()
		except Exception as e:
			raise Exception(str(e))


	def close(self):

		'''
		A method to close the sql server connection
		Example:

			>>> connection.close()
		'''

		try:
			self.connection.close()
		except Exception as exception_meassage:
			raise ConnectionError (str(exception_meassage))
		super().close()

	def refresh(self):
		'''
		A method to refresh the sql server connections

		Example:

			>>> connection.refresh()
		'''

		self.close()
		if self.trusted_connection:
			self._make_connection()
		else:
			self._make_connection(uid = self.uid, pwd = self.pwd)

