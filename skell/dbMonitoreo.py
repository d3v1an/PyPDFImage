#!/usr/bin/env python
# -*- coding: utf-8 -*

# Commons
import MySQLdb
import ast

# Config Parsers
import ConfigParser

class dbMonitoreo:

	# Configuracion de coneccion a base de datos
	DB_HOST = ''
	DB_USER = ''
	DB_PASS = ''
	DB_NAME = ''
	DB_UTF8	= False

	# Objeto de coneccion a la base de datos
	conn 	= ''

	# Cursor de coneccion
	cursor 	= ''

	def __init__(self, conf):

		# Carga de archivo de configuracion
		config = conf

		# Configurando el sistema
		self.DB_HOST = config.get('database', 'host')
		self.DB_USER = config.get('database', 'user')
		self.DB_PASS = config.get('database', 'pass')
		self.DB_NAME = config.get('database', 'db')
		self.DB_UTF8 = ast.literal_eval(config.get('database', 'utf8'))

	def connect(self):

		# Configuracion de base de datos
		conf = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME, self.DB_UTF8]

		# Conectamos a mysql
		self.conn = MySQLdb.connect(*conf)

		# Creamos cursor
		self.cursor = self.conn.cursor()

	def query(self, _query):

		# Conectamso con la base de datos
		self.connect()

		# Encodado UTF8
		if(self.DB_UTF8):
			self.conn.set_character_set('utf8')
			self.cursor.execute('SET NAMES utf8;')
			self.cursor.execute('SET CHARACTER SET utf8;')
			self.cursor.execute('SET character_set_connection=utf8;')

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