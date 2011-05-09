# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the objects library needed to insert objects into the pipe menu.

""" Here all CORE objects (labels, menus etc) """

import alan.core.actions.glob as ga

def header(text):
	""" Header """
	
	return '<separator label="%s" />' % text

def separator():
	""" A simple separator """
	
	return '<separator />'

def menu(id, label=False, objects=""):
	""" Inline menu. "objects" should already exists. """
		
	if label != False:
		label = "label=\"%s\"" % label.replace('"', '').replace("&","and")
	else:
		label = ""
	
	return """<menu id="%s" %s>
	%s
</menu>""" % (id, label, objects)

def pipemenu(id, label, command):
	""" Call a pipe menu. """
	
	return """<menu id="%s" label="%s" execute="%s" />""" % (id, label.replace('"','').replace("&","and"), command)

def item(label, action):
	""" Item. Action should already exist. """
	
	return """<item label="%s">
	%s
</item>""" % (label.replace('"',''), action)

def info(authors, sep=True):
	""" Displays informations on the extension.
	authors should be a dict which contains categories (coders, documentation etc). Every category should have another dict with a name and an email/website."""

	menus = []
	for lab,cat in authors.iteritems():
		work = []
		for aut,to in cat.iteritems():
			# Add new action and then item
			work.append(item(aut, ga.execute("xdg-open %s" % to)))
		# Add work to an ad-hoc menu
		menus.append(menu(lab, lab, "\n".join(work)))
	
	if sep:
		sep = separator() + "\n"
	else:
		sep = ""
	
	return sep + menu("informations", "Info", "\n".join(menus))
