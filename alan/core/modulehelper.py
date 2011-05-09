# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This library helps alan main executable in the process of loading a module.

def list():
	""" Lists all available modules. Usage: core.modulehelper.list(). """
	
	pass

class Extension():
	def __init__(self, modulename):
		""" The module class will represent a module. Just call this class with the module name and then invoke Module.load(). del <module> will unload the module. """
		
		self.modulename = modulename
	
	def load(self):
		# This http://stackoverflow.com/questions/951124/dynamic-loading-of-python-modules/951846#951846 is very helpful! Thanks!
		module = "alan.ext.%s" % self.modulename
		self.module = __import__(module)
		components = module.split(".")
		for comp in components[1:]:
			self.module = getattr(self.module, comp)
		
		self.mloaded = self.module
		return self.mloaded
	
	def __del__(self):
		del self.module
