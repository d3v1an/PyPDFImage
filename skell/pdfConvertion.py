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

# Configuracion
#  Parsers
import ConfigParser

class pdfConvertion:

	# Configuracion
	tName 		= ''
	mainPath 	= ''
	dataDict 	= None
	timeOut 	= 0
	is_last 	= False
	lock_file 	= None

	# Contructor
	def __init__(self, threadName, path, data_dic, is_last, lock_file):
		
		# Nombre de hilo actual
		self.tName 		= threadName

		# Path de periodicos
		self.mainPath 	= path

		# Diccionario con la informacion de los periodicos
		self.dataDict 	= data_dic

		# Saber si es el ultimo thread
		self.is_last 	= is_last

		# Archivo de lock
		self.lock_file 	= lock_file

		# Carga de archivo de configuracion
		config = ConfigParser.ConfigParser()
		config.read('pypdfimg.cfg')

		# Timeout
		self.timeOut = int(config.get('convert', 'timeout'))

	def run(self):
		# print self.test

		# Start bar as a process
		p = multiprocessing.Process(target=self.convert)
		p.start()

		# Wait for 10 seconds or until process finishes
		#p.join( (60*5) )
		p.join( self.timeOut )

		# If thread is still active
		if p.is_alive():
			
			# Eliminamos el archivo lock
			if(self.is_last):
				if os.path.exists(self.lock_file):
					os.remove(self.lock_file)

			print "Matando proceso ciclado [%s]" % (self.tName)

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
			
			# Verificamos si el directorio existe
			if(os.path.exists(full_path)):

				# Recorremos el directorio
				for _file in os.listdir(full_path):

					# Archivo PDF
					pdf_file = full_path + _file
					
					# Obtenemos la extencion del archivo
					extension = os.path.splitext(pdf_file)[1][1:]

					# Si es pdf y no contiene imagen sera procesada
					if extension == 'pdf' and not os.path.exists(pdf_file + '.jpg'):

						# Tamaño original del archivo pdf
						pdf_file_size = self.size_format(os.path.getsize(pdf_file))
						
						# Contamos las paginas del pdf
						rxcountpages 	= re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
						data 			= file(pdf_file,"rb").read()
						page_count 		= len(rxcountpages.findall(data))
						
						# Si el pdf contiene 2 paginas hacemso el merge de las mismas
						if page_count > 1 and page_count < 3:

							# Nombre base del archivo y su configuracion (Nombre y extension)
							file_data 	= os.path.splitext(os.path.basename(pdf_file))
							file_name 	= file_data[0]
							file_ext 	= file_data[1]

							# Inicio de conversion
							command = ['convert','-density','180',pdf_file,'-quality','90','-channel','RGB',pdf_file + '.jpg']
							subprocess.call(command, stdout=outfd, stderr=errfd)

							#
							#	En este punto la aplicacion crea un par de imagenes ocn nombres -1 y -2
							#

							# Se realiza el merge de las imagenes generadas
							command = ['convert','-append',full_path + file_name + '.pdf-*.jpg',pdf_file + '.jpg']
							subprocess.call(command, stdout=outfd, stderr=errfd)

							# Removemos los archivos des-unidos
							os.remove(full_path + file_name + '.pdf-0.jpg')
							os.remove(full_path + file_name + '.pdf-1.jpg')

							# Tamaño original del archivo jpg
							_jpg_size = self.size_format(os.path.getsize(pdf_file + '.jpg'))

							print "(%s) Paginas [%d] - [%s] - IMG [%s]" % (self.tName,page_count, _jpg_size, pdf_file + '.jpg')

							# optimizacion de imagen
							command = ['jpegoptim',pdf_file + '.jpg','-v','--max=80','--strip-all','-p','-t','--strip-iptc','--strip-icc']
							subprocess.call(command, stdout=outfd, stderr=errfd)

							print "(%s) Paginas [%d] - [%s] - IMG [%s]" % (self.tName,page_count, _jpg_size, pdf_file + '.jpg')

						# Si el pdf contiene 1 pagina
						if page_count == 1:

							print "(%s) Paginas [%d] - [%s] - PDF [%s]" % (self.tName,page_count, pdf_file_size, pdf_file)
							
							# Inicio de conversion
							command = ['convert','-density','180',pdf_file,'-quality','90','-channel','RGB',pdf_file + '.jpg']
							subprocess.call(command, stdout=outfd, stderr=errfd)

							# Asignacion de permisos
							if os.path.exists(pdf_file + '.jpg'):

								# Tamaño original del archivo jpg
								_jpg_size = self.size_format(os.path.getsize(pdf_file + '.jpg'))

								# Informacion del archivo convertido
								print "(%s) Paginas [%d] - [%s] - JPG [%s]" % (self.tName,page_count, _jpg_size, pdf_file + '.jpg')

								# optimizacion de imagen
								command = ['jpegoptim',pdf_file + '.jpg','-v','--max=80','--strip-all','-p','-t','--strip-iptc','--strip-icc']
								subprocess.call(command, stdout=outfd, stderr=errfd)

								# Tamaño original del archivo jpg post compress
								_jpg_size = self.size_format(os.path.getsize(pdf_file + '.jpg'))

								# Informacion del archivo convertido
								print "(%s) Paginas [%d] - [%s] - JPG [%s]" % (self.tName,page_count, _jpg_size, pdf_file + '.jpg')

								# Re asignando permisos
								self.updatePermisionsAndVisivility(pdf_file + '.jpg')

			else:
				print "(%s) Directorio [%s] no localizado" % (self.tName,full_path)

		# Eliminamos el archivo lock
		if(self.is_last):
			if os.path.exists(self.lock_file):
				os.remove(self.lock_file)

		# Cerramos los archivos de salida
		outfd.close()
		errfd.close()

	# Funcion para cambiar los permisos, usuarioy grupo de las imagenes
	def updatePermisionsAndVisivility(self,_file):

		# Cambiamos el grupo
		uid = pwd.getpwnam("captura").pw_uid
		gid = grp.getgrnam("captura").gr_gid
		os.chown(_file, uid, gid)

		# Cambiamos permisos
		os.system('chmod 777 ' + _file.replace(" ","\ "))

	# Funcion para obtener el tamaño de los archivos de manera humanizada
	def size_format(self,b):
		if b < 1000:
			return "%i" % b + 'B'
		elif 1000 <= b < 1000000:
			return "%.1f" % float(b/1000) + 'KB'
		elif 1000000 <= b < 1000000000:
			return "%.1f" % float(b/1000000) + 'MB'
		elif 1000000000 <= b < 1000000000000:
			return "%.1f" % float(b/1000000000) + 'GB'
		elif 1000000000000 <= b:
			return "%.1f" % float(b/1000000000000) + 'TB'