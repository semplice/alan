#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# Generate a menu tree.

import alan.core.structure as struct

import alan.core.config as cfg

import t9n.library as trans

import os
import __builtin__

_ = trans.translation_init("alan")

def parsename(name):
	""" Returns the appropiate name from STOCK_* """
	
	defs = {"STOCK_NULL":"", "STOCK_WEB_BROWSER":_("Web Browser"), "STOCK_TERMINAL_EMULATOR":_("Terminal Emulator"), "STOCK_APPLICATIONS":_("Applications"), "STOCK_PLACES":_("Places"), "STOCK_DESKTOP":_("Desktop"), "STOCK_LOGOUT":_("Logout"), "STOCK_EXTENSIONS":_("Extensions"), "STOCK_MUSIC":_("Music"), "STOCK_ABOUT_SEMPLICE":_("About Semplice..."), "STOCK_APPAERANCE":_("Appearance"), "STOCK_INSTALL_SEMPLICE":_("Install Semplice")}
	
	if name in defs:
		return defs[name]
	else:
		return name
	

USER = os.getenv("USER")
PWD = os.getenv("PWD")

if not os.path.exists("/usr/bin/alan-show-extension"):
	execu = "/home/g7/semplice/emily/alan/alan/alan-show-extension.py"
else:
	execu = "/usr/bin/alan-show-extension"

### THIS IS THE *MAIN* DYNAMIC MENU TREE FOR ALAN.
### This makes the menu when right-clicking on the desktop.
### YAY.

# Read configuration
conf = cfg.load_config()

## Begin with menu creation. Should read from tree.cfg
categories = conf.printv("categories","Alan").split(" ")

# Should enable icons?
icons = conf.printv("enable_icons","Alan")
if icons: os.environ["ALANICONS"] = "True"

# Load objects now
import alan.core.objects.core as core
import alan.core.actions.glob as ga

# Create menu object
menu = struct.PipeMenu()
menu.start()

# alias insert
i = menu.insert

# Header
i(core.header(USER))

# Begin creating menu
for cat in categories:
	if cat == "-":
		# Separator
		i(core.separator)
		continue

	# Check if this is a main menu (@)
	if cat[0] == "@":
		# True.
		IS_MAIN = True
		
		# Depure name
		cat = cat[1:]
	else:
		IS_MAIN = False

	conf.module = "cat:%s" % cat # Change default section
	name = parsename(conf.printv("name"))
	extensions = conf.printv("extensions").split(" ")
	icon = conf.printv("icon")
	if not icons or not icon: icon = ""
		
	items = []
	for ext in extensions:
		# Generate extension
		conf.module = "ext:%s" % ext # Change default section
		
		if ext == "-":
			# Separator
			items.append(core.separator)
		else:
			# Normal extension
			_name = parsename(conf.printv("name")) # Get name
			_ext = conf.printv("ext") # Get real extension name
			
			_icon = conf.printv("icon")
			if not icons or not _icon: _icon = ""
			
			if _ext == "__itemlist__":
				# Create item list
				
				# If name, create an header
				if _name:
					items.append(core.header(_name))
				
				count = int(conf.printv("count"))
				done = 0
				while done != count:
					# Create items
					done += 1

					# Get object icon
					_icon = conf.printv("icon%s" % done)
					if not icons or not _icon: _icon = ""

					items.append(core.item(parsename(conf.printv("item%s" % done)), ga.execute(conf.printv("item%s_ex" % done)), icon=_icon))
			elif _ext == "__menu__":
				# Internal menu id
				items.append(core.menu(conf.printv("id"), icon=_icon))
			elif _ext == "__item__":
				# Normal menu item
				items.append(core.item(parsename(conf.printv("name")), ga.execute(conf.printv("executable")), icon=_icon))
			else:
				# An external extension
				items.append(core.pipemenu(ext, _name, "%s %s" % (execu,ext), icon=_icon))
	
	if IS_MAIN:
		# We are main? The items should not be in submenu.
		i("\n".join(items))
	else:
		# Generate a submenu and then add the items.
		i(core.menu(cat, name, "\n".join(items), icon=icon))
	

menu.end()
print menu.final_menu
