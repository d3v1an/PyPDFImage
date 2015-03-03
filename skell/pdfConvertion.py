#!/usr/bin/env python
# -*- coding: utf-8 -*

# Common
import os
import subprocess
import pwd
import grp
import sys
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
		p.join(10)

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
				for _file in os.listdir(full_path):
					print _file
			else:
				print "Directorio [%s] no localizado" & (full_path)

			# print(full_path)
			# print("%s/%s/%s/" % (self.mainPath,_dir[0].strip().strip('\n\r'),_dir[1]))

		# for i in range(100):
		# 	print "Tick " + self.test 
		# 	time.sleep(1)