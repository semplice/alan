# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the structure library needed to make a correct pipe menu.

import os
import alan.core.hashme as hashme

HOME = os.getenv("HOME")

class PipeMenu:
	def __init__(self, use_cache=False, cache=None, cache_trigger=(), cache_path=None):
		# New pipe menu
		self.menu = []
		
		# Use cache?
		self.use_cache = use_cache
		self.cache = cache
		self.cache_trigger = cache_trigger
		if cache_path == None:
			self.cache_path = os.path.join(HOME, ".config/alan")
		else:
			self.cache_path = cache_path
		if use_cache:
			if os.getenv("ALANICONS"):
				# use icons, trigger the gtkrc.
				self.cache_trigger = self.cache_trigger + (os.path.join(HOME, ".gtkrc-2.0"),)
		
		self.cache_loaded = False
	
	def cache_check(self):
		""" Checks for the cache. Returns True if everything is up-to-date, False if not. """
				
		if not self.use_cache:
			return False
				
		md5s = {}
		for trigger in self.cache_trigger:
			if not os.path.exists(trigger):
				# Trigger doesn't exist. False.
				return False
			md5 = hashme.md5()
			md5 = md5.file(trigger)
			md5s[trigger] = md5
			
		_file = os.path.join(self.cache_path, ".%s.md5" % self.cache)
		_cachefile = os.path.join(self.cache_path, ".%s.cache" % self.cache)
		if not os.path.exists(_cachefile):
			# The cachefile does not exist. False.
			return False

		if os.path.exists(_file):
			with open(_file) as f:
				lines = f.readlines()
			
			md5f = {}
			# New dict with md5s on lines:
			for line in lines:
				line = line.split(":")
				md5f[line[0]] = line[1].replace("\n","")
			
			# Compare items
			for item, md5 in md5s.items():
				try:
					if not md5f[item] == md5:
						# At least one wrong, should recache.
						return False
				except:
					return False # something is missing, rebuild cache.
			
		else:
			# md5 file doesn't exist, recache.
			return False
		
		# If we are here, everything went well.
		return True
	
	def cache_read(self):
		""" Reads and outputs the cache. """
		
		_file = os.path.join(self.cache_path, ".%s.cache" % self.cache)
		with open(_file) as f:
			self.menu = f.readlines()
		
		self.cache_loaded = True
		
	def insert(self, value):
		""" New line in self.menu. """
		
		# Split lines, if more than one
		if "\n" in value:
			value = value.split("\n")
		else:
			value = [value]
		
		# Finally insert
		self.menu += value
	
	def start(self):
		""" Inserts the tag <openbox_pipe_menu> to self.menu """
		
		self.insert("<openbox_pipe_menu>")
	
	def end(self):
		""" Ends tag inserted by start. """
		
		self.insert("</openbox_pipe_menu>")
	
	@property
	def final_menu(self):
		""" Prints the menu """
		
		if self.use_cache and not self.cache_loaded:
			# Write the cache file.
			_file = os.path.join(self.cache_path, ".%s.md5" % self.cache)
			_cachefile = os.path.join(self.cache_path, ".%s.cache" % self.cache)
			
			with open(_cachefile, "w") as f:
				f.write("\n".join(self.menu))
						
			with open(_file, "w") as f:
				for trigger in self.cache_trigger:
					md5 = hashme.md5()
					md5 = md5.file(trigger)
					
					f.write("%s:%s\n" % (trigger,md5))
		
		return "\n".join(self.menu)
