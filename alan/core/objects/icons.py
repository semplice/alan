# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the objects library needed to insert objects into the pipe menu.

""" Here all CORE objects (labels, menus etc) """

size = 64 # Ovverride this using the size argument on any function.

import os

enabled = os.getenv("ALANICONS")

if enabled:
	#from gi.repository.Gtk import IconTheme
	from gtk import icon_theme_get_default, ICON_LOOKUP_NO_SVG

def get_stock_icon(icon, size=size):
	""" Gets an icon from the STOCK GTK+ icons repository.
	Use get_icon() instead. It will call this def when needed. """
	
	#theme = IconTheme.new()
	theme = icon_theme_get_default()
	icon = theme.lookup_icon(icon.replace(".png","").replace(".xpm","").replace(".svg",""), size, ICON_LOOKUP_NO_SVG)
	
	if icon:
		return icon.get_filename()
	else:
		return None

def get_icon(icon, size=size):
	""" Examinates an icon, then returns an appropriate filename. """
	
	if not enabled: return None
	
	icon = os.path.expanduser(icon)
	
	if icon[0] == "/":
		# Not a stock icon
		if os.path.exists(icon):
			return icon
		else:
			return None
	else:
		return get_stock_icon(icon, size)
