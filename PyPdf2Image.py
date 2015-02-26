#!/usr/bin/env python
# -*- coding: utf-8 -*

import MySQLdb
import time
import os
import subprocess
import pwd
import grp
import sys

class Pdf2Image:

	# Configuracion de coneccion a base de datos
	DB_HOST = 'localhost'
	DB_USER = 'root'
	DB_PASS = 'Gaddp552014'
	DB_NAME = 'monitoreoGa'

	# Mensage de inicializacion
	welcome = "Ejecutando Script para exportar PDF's a Imagenes"

	# Propiedades relativas al formato 
	divline = "="*80

	# Método constructor 
	def __init__(self):

		# Verificamos que no exista el archivo lock
		lock_file = os.path.dirname(os.path.abspath(__file__)) + '/PyPdf2Image.lock'

		if os.path.exists(lock_file):
			print "El sistema ya se encuentra ejecutandose"
			sys.exit()

		# Bloqueamos la ejecucion
		open(lock_file, 'w').close()
		
		print self.divline
		print "\t" + self.welcome
		print self.divline
		print "\n\tFehca de busqueda de archivos : " + time.strftime("%Y-%m-%d")
		print "\tFecha y hora de ejecucion del script : " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print self.divline
		
		# Inicio de ejecucion del script
		start_time = time.time()

		# Query para lectura de directorios
		query = """SELECT DISTINCT(ruta) rutas FROM (
				SELECT CONCAT('/var/www/siscap.la/public/Periodicos/',p.Nombre,'/',n.Fecha,'/') AS 'ruta', 'noticias' AS 'tipo' FROM noticiasDia n, periodicos p
                WHERE Fecha = CURDATE() AND idCapturista NOT IN(28) AND Categoria!=80 AND (n.Periodico=p.idPeriodico)
                UNION ALL
                SELECT CONCAT('/var/www/siscap.la/public/Periodicos/',p.Nombre,'/',n.Fecha,'/') AS 'ruta', 'anuncios' AS 'tipo'
                FROM anunciosDia n, periodicos p
                WHERE Fecha = CURDATE() AND idCapturista NOT IN(28) AND Categoria!=80 AND (n.Periodico=p.idPeriodico)
            ) AS t1"""
		
		# Ejecucion de proceso de query
		result = self.run_query(query);

		# Recorremos los directorios
		for directory in result:
			# Una ves listados los archivos buscamos y eliminamos los archivos grandes
			print "\tProcesando el directorio \t: " + directory[0]
			self.proccessDir(directory[0])

		# Impresion de finalizacion de ejecucion
		print("--- %.5f Segundos en ejecucion ---" % (time.time() - start_time))
		print "\n" + self.divline
		print "\tFecha y hora de finalizacion de ejecucion del script : " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print self.divline

		if os.path.exists(lock_file):
			os.remove(lock_file)

	# Funcion para ejecutar un query
	def run_query(self,query=''):

		# Configuracion de base de datos
		datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

		# Conectamos a mysql
		conn = MySQLdb.connect(*datos)

		# Creamos cursor
		cursor = conn.cursor()

		# Ejecutamos el query
		cursor.execute(query)

		# Si es un select hacemos un fetchall
		# de lo contrario hacemos un commit del comando
		if query.upper().startswith('SELECT'): 
			data = cursor.fetchall()
		else:
			conn.commit()
			data = None

		# Cerramos el cursor y coneccion a la base de datos
		cursor.close()
		conn.close()

		return data

	# Funcion para procesar los directorios
	def proccessDir(self,_dir):

		# Archivos de salida
		outfd = open('file_out', 'w+')
		errfd = open('file_err', 'w+')

		# Listamos los archivos del directorio
		for _file in os.listdir(_dir):
			
			# Obtenemos la extencion del archivo
			extension = os.path.splitext(_dir + _file)[1][1:]

			# Si es pdf sera procesada
			if extension == 'pdf' and not _file[:5].lower().strip()== 'todas' and not os.path.exists(_dir + _file + '.jpg'):

				# Tamaño original del archivo pdf
				_pdf_size = self.size_format(os.path.getsize(_dir + _file))

				# Ejecutando proceso de conversion
				print "\tConvertiendo el archivo \t: " + _file + ' ' + _pdf_size
				command = ['convert','-density','180','-trim',_dir + _file,'-quality','90','-channel','RGB',_dir + _file + '.jpg']
				subprocess.call(command, stdout=outfd, stderr=errfd)

				if os.path.exists(_dir + _file + '.jpg'):
					# Re asignando permisos
					self.updatePermisionsAndVisivility(_dir + _file + '.jpg')

					# Tamaño original del archivo jpg
					_jpg_size = self.size_format(os.path.getsize(_dir + _file + '.jpg'))

					# Informacion del archivo convertido
					print "\tArchivo convertido \t\t: " + _file + '.jpg ' + _jpg_size

		# Cerramos los archivos de salida
		outfd.close()
		errfd.close()

		# Leemos el archivo de salida
		fd = open('file_out', 'r')
		output = fd.read()
		fd.close()

		# Leemos el archivo de error
		fd = open('file_err', 'r')
		err = fd.read()
		fd.close()

	# Funcion para cambiar los permisos, usuarioy grupo de las imagenes
	def updatePermisionsAndVisivility(self,_file):

		# Cambiamos el grupo
		uid = pwd.getpwnam("captura").pw_uid
		gid = grp.getgrnam("captura").gr_gid
		os.chown(_file, uid, gid)

		# Cambiamos permisos
		os.system('chmod 777 ' + _file.replace(" ","\ "))
		#os.chmod(_file, 0777)

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

if __name__ == '__main__':
    # Instanciar clase 
	p2i = Pdf2Image()
