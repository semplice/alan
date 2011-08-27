#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#

import alan.core.modulehelper as mod
import alan.core.config as cfg
import sys, os

import t9n.library

_ = t9n.library.translation_init("alan")

def error(text):
	""" Display an error if something went wrong. """
	
	import alan.core.structure as struct
	import alan.core.objects.core as core
	
	menu = struct.PipeMenu()
	menu.start()
	
	menu.insert(core.item(text,""))
	
	menu.end()
	
	print menu.final_menu


# Load module by reading sys.argv[1]

if len(sys.argv) < 2:
	extension_not_found()
	sys.exit()

name = sys.argv[1]

# Read configuration file, and search for name
cfg = cfg.load_config("ext:%s" % name)

# Get extension name:
ext = cfg.printv("ext")

# Should use icons?
if cfg.printv("enable_icons","Alan"):
	os.environ["ALANICONS"] = "True"

# Load module
try:
	module = mod.Extension(ext)
	loaded = module.load(cfg)
	
	# Print menu
	print loaded.menu.final_menu
except ImportError:
	error(_("Module not found!"))
except:
	error(_("An error occurred while running the module."))
finally:
	sys.exit()
