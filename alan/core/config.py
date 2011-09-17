# -*- coding: utf-8 -*-
# pylaivng core config module - (C) 2010 Eugenio "g7" Paolantonio and the µSoft Team.
# All rights reserved. Work released under the GNU GPL license, version 3 or later.
#
# This is a module of pylaivng, should not be executed as a standalone application.

import os

try:
	import ConfigParser as cparser # Python 2.x
except:
	import configparser as cparser # Python 3.x

class Config:
	def __init__(self, file, initial=False):
		""" This class will read a configfile. /etc/pylaivng is already inserted, so for file you only need to pass subdirectory and file, for example distributions/semplice. """
		
		self.path = file
		self.initial = initial
		if not initial:
			if not os.path.exists(self.path):
				raise Exception(self.path + " does not exist!")
		
		# Open the file, if it is initial just open it in ram...
		self.config = cparser.SafeConfigParser()
		if not initial:
			self.config.read(self.path)
	
	def has_section(self, section):
		""" This function will check if section 'section' is present into the config file. """
		return self.config.has_section(section)
	
	def has_option(self, section, option):
		""" This function will check if option is present into the section 'section' into the config file."""
		return self.config.has_option(section, option)
	
	def get(self, section, thing):
		""" This function will get a value from the configfile. """
		return self.config.get(section, thing)
	
	def add(self, section):
		""" This function will add a section in the configfile. """
		self.config.add_section(section)
	
	def set(self, section, thing, value):
		""" This function will set a value in the configfile. """
		self.config.set(section, thing, value)
	
	def commit(self):
		""" Write changes to the config file. """
		with open(self.path,"w") as configfile:
			self.config.write(configfile)
	
	def __del__(self):
		""" Cleanup """
		del self.config

class ConfigRead(Config):
	""" Simple class to read config files. """
	def __init__(self, file, module=False):
		
		Config.__init__(self, file, False)
		self.module = module # Module ("section") name.
	
	def printv(self, opt, section=False):
		""" This function will get the requested value from section. """
		
		# If section = false, copy the default self.module, if any
		if not section:
			section = self.module
		
		if self.has_option(section, opt):
			opt = self.get(section, opt)
			if opt.lower() == "true":
				return True
			elif opt.lower() == "false":
				return False
			elif opt.lower() == "none":
				return None
			else:
				return opt
		else:
			return False

def load_config(module=False):
	""" Returns a loaded ConfigRead object. """
	
	HOME = os.getenv("HOME")
	
	if not os.path.exists(os.path.join(HOME, ".config/alan/tree.conf")):
		## Use default configuration
		conf = "/etc/alan/tree.conf"
	else:
		conf = os.path.join(HOME, ".config/alan/tree.conf")
	
	return ConfigRead(conf, module=module)

