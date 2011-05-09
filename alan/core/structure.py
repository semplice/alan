# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the structure library needed to make a correct pipe menu.

class PipeMenu:
	def __init__(self):
		# New pipe menu
		self.menu = []
	
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
	
	def printm(self):
		""" Prints the menu """
		
		print "\n".join(self.menu)
