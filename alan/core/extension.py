# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the base extension class that will be used by any extension.

class Extension:
	def __init__(self, cfg):
		""" Init definition.
		
		cfg is the ConfigRead object. alan-show-extension should pass it.
		"""
		
		self.menu = False
		
		self.cfg = cfg
		self.run()
	
	def run(self):
		""" Run the extension. Extensions should override this definition!"""
		
		pass
