# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the objects library needed to insert objects into the pipe menu.

""" Here all CORE objects (labels, menus etc) """

import alan.core.actions.glob as ga
import alan.core.objects.icons as ico
import t9n.library as trans

_ = trans.translation_init("alan")

def header(text):
	""" Header """
	
	return '<separator label="%s" />' % text

#def separator():
#	""" A simple separator """
#	
#	return '<separator />'

separator = "<separator />"

def menu(id, label="", objects="", icon=""):
	""" Inline menu. "objects" should already exists. """
		
	if label:
		label = "label=\"%s\"" % label.replace('"', '').replace("&","&amp;")
	
	if icon and ico.get_icon(icon):
		icon = "icon=\"%s\"" % ico.get_icon(icon)
	else:
		icon = ""
	
	return """<menu id="%s" %s %s>
	%s
</menu>""" % (id, label, icon, objects)

def pipemenu(id, label, command, icon=""):
	""" Call a pipe menu. """

	if icon and ico.get_icon(icon):
		icon = "icon=\"%s\"" % ico.get_icon(icon)
	else:
		icon = ""

	return """<menu id="%s" label="%s" execute="%s" %s />""" % (id, label.replace('"','').replace("&","&amp;"), command, icon)

def item(label, action, icon=""):
	""" Item. Action should already exist. """

	if icon and ico.get_icon(icon):
		icon = "icon=\"%s\"" % ico.get_icon(icon)
	else:
		icon = ""

	return """<item label="%s" %s>
	%s
</item>""" % (label.replace('"','').replace("&","&amp;"), icon, action)

def info(authors, sep=True, icon=False):
	""" Displays informations on the extension.
	authors should be a dict which contains categories (coders, documentation etc). Every category should have another dict with a name and an email/website."""

	if icon:
		icon = "gtk-about"

	menus = []
	for lab,cat in authors.iteritems():
		work = []
		for aut,to in cat.iteritems():
			# Add new action and then item
			work.append(item(aut, ga.execute("xdg-open %s" % to)))
		# Add work to an ad-hoc menu
		menus.append(menu(lab, lab, "\n".join(work)))
	
	if sep:
		sep = separator + "\n"
	else:
		sep = ""
	
	return sep + menu("informations", _("Info"), "\n".join(menus), icon=icon)
