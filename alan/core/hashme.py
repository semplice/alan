# -*- coding: utf-8 -*-
# pylaivng hashme library - (C) 2010 Eugenio "g7" Paolantonio and the µSoft Team.
# All rights reserved. Work released under the GNU GPL license, version 3 or later.
#
# This is a module of pylaivng, should not be executed as a standalone application.

import hashlib

""" Convenience library to get hashes of a file """

class Engine:
	def __init__(self, obj, bits):
		""" Main engine of hashme.
		
		Parameters:
		obj: hashlib object (e.g.: haslib.md5, haslib.sha1)
		bits: bits to read for each line
		"""
		
		self.obj = obj # The object used, running.
		#self.normal_obj = obj # The object unused.
		self.bits = bits
	
	def file(self, _file):
		""" Calculates hash of a file.
		
		Parameters:
		_file: file to get hash from """
		
		# Open file
		opened = open(_file, "rb")
		
		# Infinite loop which reads the defined bits on the file (and updates the object).
		while True:
			# Read the bits
			buff = opened.read(self.bits)
			if not buff:
				# If the buff is empty, it is EOF. So, break the loop.
				break
			
			# Update object
			self.obj.update(buff)
		
		# Close file
		opened.close()
		
		# Return hash
		return self.obj.hexdigest()

class md5(Engine):
	def __init__(self):
		""" The md5sum hash calculator. Derivative of the Engine class.
		
		To calculate the md5 of a file, use md5.file(<filename>)."""
		
		# __init__ of Engine with our values
		Engine.__init__(self, hashlib.md5(), 32768) # * 256

class sha1(Engine):
	def __init__(self):
		""" The sha1sum hash calculator. Derivative of the Engine class.
		
		To calculate the sha1 of a file, use sha1.file(<filename>)."""
		
		# __init__ of Engine with our values
		Engine.__init__(self, hashlib.sha1(), 40960) # * 256
