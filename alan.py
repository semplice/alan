#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#

import alan.core.modulehelper as mod
import sys

def extension_not_found():
	""" when extension is not found, do this. """
	
	import alan.core.structure as struct
	import alan.core.objects.core as core
	
	menu = struct.PipeMenu()
	menu.start()
	
	menu.insert(core.item("Module is not found!",""))
	
	menu.end()
	
	menu.printm()


# Load module by read sys.argv[1]

if len(sys.argv) < 2:
	extension_not_found()
	sys.exit()

ext = sys.argv[1]

# Load module
try:
	module = mod.Extension(ext)
	loaded = module.load()
except:
	extension_not_found()
	sys.exit()
