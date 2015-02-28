#!/usr/bin/env python
# -*- coding: utf-8 -*

# Modulos
import threading
import time

# Flag d salida?
exitFlag = 0

# Clase threading
class d3Thread (threading.Thread):

	# Configuracion de thread
	threadID	= 0
	threadName	= ''
	dataDict	= {}

	# Contructor
	def __init__(self, threadID, name, dataDict):
		threading.Thread.__init__(self)
		self.threadID 	= threadID
		self.threadName	= name
		self.dataDict	= dataDict

	# Despliegue de aplicacion
	def run(self):
		print "Starting " + self.threadName + " convertions"
		self.print_time(self.threadName, 3, 5)
		print "Exiting " + self.threadName + " convertions"

	# Funcion de prueba
	def print_time(self, threadName, delay, counter):
		while counter:
			if exitFlag:
				thread.exit()
			time.sleep(delay)
			print "%s: %s\r" % (threadName, time.ctime(time.time()))
			counter -= 1