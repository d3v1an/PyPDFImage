#!/usr/bin/env python
# -*- coding: utf-8 -*

# Modulos
import threading
import time

# Configuracion
#  Parsers
import ConfigParser

# D3
from pdfConvertion import *

# Flag d salida?
exitFlag = 0

# Clase threading
class d3Thread (threading.Thread):

	# Configuracion de thread
	threadID	= 0
	threadName	= ''
	dataDict	= {}
	mainPath 	= ''
	is_last 	= False
	config 		= None

	# Contructor
	def __init__(self, threadID, name, dataDict, is_last, conf):

		# Configuracion de thread
		threading.Thread.__init__(self)
		self.threadID 	= threadID
		self.threadName	= name
		self.dataDict	= dataDict
		self.is_last 	= is_last

		# Carga de archivo de configuracion
		self.config = conf

		# Directorio principal
		self.mainPath = self.config.get('paths', 'periodicos')

	# Despliegue de aplicacion
	def run(self):

		# Inicio de ejecucion del hilo
		start_time = time.time()
		print("Inicio de hilo (%s) de conversión de periódicos." % (self.threadName))
		self.convertion(self.threadName)
		print("Fin de hilo (%s) de conversión de periódicos. Tiempo de ejecusion (%.5f segundos)" % (self.threadName, (time.time() - start_time)))

	# Funcion de prueba
	def convertion(self, threadName):
		
		# Despliegue de aplicacion
		p2i = pdfConvertion(threadName, self.mainPath, self.dataDict, self.is_last, self.config)
		p2i.run()