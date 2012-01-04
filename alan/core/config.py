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
		self.is_fork = False
		if not initial:
			if not os.path.exists(self.path):
				raise Exception(self.path + " does not exist!")
		
		# Open the file, if it is initial just open it in ram...
		self.config = cparser.SafeConfigParser()
		if not initial:
			self.config.read(self.path)

		# Should check if it is a fork
		if not initial:
			if self.has_section("Alan:extends"):
				# The fork section is there...
				if self.has_option("Alan:extends","source"):
					# Ok, the source option is there. We should get it and load the source configuration file, too.
					self.source = str(self.get("Alan:extends","source"))
					
					# Yes! this is a fork
					self.is_fork = True
					
					# Load source
					self.config.read(self.source)
					self.config.read(self.path) # Read again the fork.

	def _diff_original_changed(self, original, changed):
		""" Returns a list of changed values into the 'changed' object. (INTERNAL) """

		orig_sections = original.sections() # get all sections of original.
		chan_sections = changed.sections() # get all sections of changed.
		
		changed_options = []
		added_sections = []
		
		for sect in chan_sections:
			# Check if sect exists on original...
			if original.has_section(sect):
				# Original has the section
				chan_options = changed.options(sect) # get all options
				for opt in chan_options:
					if original.has_option(sect, opt):
						# original has option, check if it is changed...
						if changed.get(sect, opt) != original.get(sect, opt):
							# Something has changed...
							changed_options.append((sect, opt, changed.get(sect, opt)))
					else:
						# Option not found in original, so we should add it.
						changed_options.append((sect, opt, changed.get(sect, opt)))
			else:
				# Section not found in original, we should add that + all options...
				added_sections.append(sect)
				for opt in changed.options(sect):
					changed_options.append((sect, opt, changed.get(sect, opt)))
		
		# We should check all options and see if the section of them is into the *original fork file*
		#for opt in changed_options:
		#	if not original_fork.has_section(opt[0]):
		#		# We should add it to added_sections
		#		added_sections.append(opt[0])
		
		return added_sections, changed_options
	
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
		# Currently disable commit if this is a fork
		if not self.is_fork:
			with open(self.path,"w") as configfile:
				self.config.write(configfile)
		else:
			# We should write only the changed things.

			# We should load again a clean source + fork and then make a diff...
			# Load source
			self.diff_config_source = cparser.SafeConfigParser()
			self.diff_config_source.read(self.source)
			
			# Load fork
			self.diff_config_source.read(self.path)
			
			# diff
			sect, opts = self._diff_original_changed(self.diff_config_source, self.config)
									
			if opts:
				# There are some new options, so we can continue...
				
				# Load again the fork, but not merge it.
				self.to_write = cparser.SafeConfigParser()
				self.to_write.read(self.path)
				
				# First add sections...
				if sect:
					# If we should add sections, add them now.
					for s in sect:
						self.to_write.add_section(s)
				
				# Now add options...
				for o in opts:
					# If section does not exists, add it now.
					if not self.to_write.has_section(o[0]):
						self.to_write.add_section(o[0])
					self.to_write.set(o[0], o[1], o[2])
				
				# Now really write...
				with open(self.path,"w") as configfile:
					self.to_write.write(configfile)

	
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

