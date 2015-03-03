#!/usr/bin/env python
# -*- coding: utf-8 -*

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