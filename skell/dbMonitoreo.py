#!/usr/bin/env python
# -*- coding: utf-8 -*

#  Commons
import MySQLdb

#  Parsers
import ConfigParser

class dbMonitoreo:

	# Configuracion de coneccion a base de datos
	DB_HOST = ''
	DB_USER = ''
	DB_PASS = ''
	DB_NAME = ''

	# Objeto de coneccion a la base de datos
	conn 	= ''

	# Cursor de coneccion
	cursor 	= ''

	def __init__(self):

		# Carga de archivo de configuracion
		config = ConfigParser.RawConfigParser()
		config.read('pypdfimg.cfg')

		# Configurando el sistema
		self.DB_HOST = config.get('database', 'host')
		self.DB_USER = config.get('database', 'user')
		self.DB_PASS = config.get('database', 'pass')
		self.DB_NAME = config.get('database', 'db')

	def connect(self):

		# Configuracion de base de datos
		conf = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

		# Conectamos a mysql
		self.conn = MySQLdb.connect(*conf)

		# Creamos cursor
		self.cursor = self.conn.cursor()

	def query(self, _query):

		# Conectamso con la base de datos
		self.connect()

		# Query para periodicos del estado de mexico y df?
		query = _query

		# Ejecutamos el query
		self.cursor.execute(query)

		# Contenedor de resultados de la ejecucion del query
		data = self.cursor.fetchall()

		# Cerramos el cursor y coneccion a la base de datos
		self.cursor.close()
		self.conn.close()

		return data