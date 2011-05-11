#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# Generate a menu tree.

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga

import alan.core.config as cfg

import alan.core.translations as trans

import os

_ = trans.translation_init("alan")

def parsename(name):
	""" Returns the appropiate name from STOCK_* """
	
	defs = {"STOCK_NULL":"", "STOCK_WEB_BROWSER":_("Web Browser"), "STOCK_TERMINAL_EMULATOR":_("Terminal Emulator"), "STOCK_APPLICATIONS":_("Applications"), "STOCK_PLACES":_("Places"), "STOCK_DESKTOP":_("Desktop"), "STOCK_LOGOUT":_("Logout"), "STOCK_EXTENSIONS":_("Extensions"), "STOCK_MUSIC":_("Music"), "STOCK_ABOUT_SEMPLICE":_("About Semplice..."), "STOCK_APPAERANCE":_("Appearance")}
	
	if name in defs:
		return defs[name]
	else:
		return name
	

USER = os.getenv("USER")
PWD = os.getenv("PWD")

if not os.path.exists("/usr/bin/alan-show-extension.py"):
	execu = "/home/g7/semplice/emily/alan/alan-show-extension.py"
else:
	execu = "/usr/bin/alan-show-extension.py"

if not os.path.exists("/usr/share/alan/tree.cfg"):
	conf = "/home/g7/semplice/emily/alan/tree.cfg"
else:
	conf = "/usr/share/alan/tree.cfg"

### THIS IS THE *MAIN* DYNAMIC MENU TREE FOR ALAN.
### This makes the menu when right-click on the desktop.
### YAY.

# Read configuration
conf = cfg.ConfigRead(conf)

# Create menu object
menu = struct.PipeMenu()
menu.start()

# alias insert
i = menu.insert

# Header
i(core.header(USER))

## Begin with menu creation. Should read from tree.cfg
categories = conf.printv("categories","Alan").split(" ")

# Begin creating menu
for cat in categories:
	conf.module = "cat:%s" % cat # Change default section
	name = parsename(conf.printv("name"))
	extensions = conf.printv("extensions").split(" ")
		
	items = []
	for ext in extensions:
		# Generate extension
		conf.module = "ext:%s" % ext # Change default section
		_name = parsename(conf.printv("name"))
		
		if "_itemlist_" in ext:
			# Create item list
			count = int(conf.printv("count"))
			fatte = 0
			while fatte != count:
				# Create items
				fatte += 1
				items.append(core.item(parsename(conf.printv("item%s" % fatte)), ga.execute(conf.printv("item%s_ex" % fatte))))
		elif ext == "-":
			# Separator
			items.append(core.separator())
		elif "_menu_" in ext:
			# Internal menu id
			items.append(core.menu(conf.printv("id")))
		elif "_item_" in ext:
			# Normal menu item
			items.append(core.item(parsename(conf.printv("name")), ga.execute(conf.printv("executable"))))
		else:
			# Is a normal extension, create a pipemenu
			items.append(core.pipemenu(ext, _name, execu + " %s" % ext))
	
	if "main_" in cat:
		# We are main? The items should not be in submenu.
		i("\n".join(items))
	else:
		# Generate a submenu and then add the items.
		i(core.menu(cat, name, "\n".join(items)))
	

menu.end()
menu.printm()
