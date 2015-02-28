#!/usr/bin/env python
# -*- coding: utf-8 -*

# Modulos
#  Threads
import thread
import time

# Configuracion
#  Parsers
import ConfigParser
import ast

#  Commons
import os
import subprocess
import pwd
import grp
import sys

# Librerias
from common.utils import *
from skell.dbMonitoreo import *
from skell.d3Thread import *

# Clase para el tratado de imagenes y pdf's
class Pdf2Image:

	# Configuracion de conversion pdf > img
	DENSITY = ''
	QUALITY = ''
	CHANNEL = ''

	# Mensage de inicializacion
	WELCOME = "Ejecutando Script para exportar PDF's a Imagenes (V2)"

	# Propiedades relativas al formato 
	DIVLINE = "="*80

	# Contenedor de clase para el monitoreo de periodicos
	dbm 	= ''

	# Objeto de configuracion
	config 	= ''

	# Método constructor 
	def __init__(self):

		# Carga de archivo de configuracion
		self.config = ConfigParser.ConfigParser()
		self.config.read('pypdfimg.cfg')

		# Asignacion de clase conectora a db
		self.dbm = dbMonitoreo()

		# Mensaje de bienvenida
		print self.DIVLINE
		print "\t" + self.WELCOME
		print self.DIVLINE
		print "\n\tFehca de busqueda de archivos : " + time.strftime("%Y-%m-%d")
		print "\tFecha y hora de ejecucion del script : " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print self.DIVLINE

	def run(self):
		
		# Inicio de ejecucion del script
		start_time 	= time.time()

		# Contenedor de resultados de consulta
		data 		= ''

		# Diccionario de threads
		tDict = {}

		# Obtenemos los queris que necesitamos consultar x cada thread
		queries = ast.literal_eval(self.config.get('database', 'queries'))
	
		# Recorremos el resultado de los queries
		i = 1
		for k in queries:

			# Obtenemos los periodicos y la fecha actual
			periodicos = self.dbm.query(queries[k])

			# Creamos los threads por cada query
			tDict[k] = d3Thread(i,k,periodicos)
			i += 1

			tDict[k].start()

			# Recorremos cada periodico
			# for p in periodicos:

				# En este punto crearemos un hilo pr cada serie de periodicos
				# postereormente se procezara 
				# print p[0], " ", p[1], "\r"

if __name__ == '__main__':

	pio = Pdf2Image()
	pio.run()