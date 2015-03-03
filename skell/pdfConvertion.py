#!/usr/bin/env python
# -*- coding: utf-8 -*

# Common
import os
import subprocess
import pwd
import grp
import sys
import re

# Multi proceso
import multiprocessing
import time

class pdfConvertion:

	# Configuracion
	tName 		= ''
	mainPath 	= ''
	dataDict 	= None

	# Contructor
	def __init__(self, threadName, path, data_dic):
		
		# Nombre de hilo actual
		self.tName 		= threadName

		# Path de periodicos
		self.mainPath 	= path

		# Diccionario con la informacion de los periodicos
		self.dataDict 	= data_dic

		# for _dir in self.dataDict:
		# 	print("%s - /%s/%s/" % (threadName,_dir[0].strip().strip('\n\r'), _dir[1]))
		# while counter:
		# 	if exitFlag:
		# 		thread.exit()
		# 	time.sleep(delay)
		# 	print "%s: %s\r" % (threadName, time.ctime(time.time()))
		# 	counter -= 1

	def run(self):
		# print self.test

		# Start bar as a process
		p = multiprocessing.Process(target=self.convert)
		p.start()

		# Wait for 10 seconds or until process finishes
		p.join( (60*5) )

		# If thread is still active
		if p.is_alive():
			print "running... let's kill it... " + self.tName

		# Terminate
		p.terminate()
		p.join()

	# Conversion de archivos
	def convert(self):

		# Archivos de salida
		outfd = open('file_out', 'w+')
		errfd = open('file_err', 'w+')
		
		# Recorremos todos los directorios
		for _dir in self.dataDict:

			# Path principal
			full_path = "%s%s/%s/" % (self.mainPath,_dir[0].strip().strip('\n\r'),_dir[1])
			
			# Verificamos si el directorio exuste
			if(os.path.exists(full_path)):

				# Recorremos el directorio
				for _file in os.listdir(full_path):
					
					# Obtenemos la extencion del archivo
					extension = os.path.splitext(full_path + _file)[1][1:]

					# Si es pdf y no contiene imagen sera procesada
					if extension == 'pdf' and not os.path.exists(full_path + _file + '.jpg'):
						
						# Contamos las paginas del pdf
						rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
						data = file(full_path + _file,"rb").read()
						page_count = len(rxcountpages.findall(data))
						
						if page_count > 1:
							print "Paginas [%d] - PDF [%s]" % (page_count, full_path + _file)

			else:
				print "Directorio [%s] no localizado" % (full_path)

			# print(full_path)
			# print("%s/%s/%s/" % (self.mainPath,_dir[0].strip().strip('\n\r'),_dir[1]))

		# for i in range(100):
		# 	print "Tick " + self.test 
		# 	time.sleep(1)