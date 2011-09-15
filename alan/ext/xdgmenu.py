# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 2 or later.
#
# This file cointain the xdgmenu extension

#### BASED ON xdg-menu.py from fedora
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Luke Macken <lmacken@redhat.com>
#            Miroslav Lichvar <mlichvar@redhat.com>
####

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga

import alan.core.extension

import sys, os

import gmenu, re, sys
from xml.sax.saxutils import escape

# Informations about extension ;)
coders = { "Luke Macken (xdg-menu.py)":"mailto:lmacken@redhat.com", "Miroslav Lichvar (xdg-menu.py)":"mailto:mlichvar@redhat.com", "Eugenio \"g7\" Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

class Extension(alan.core.extension.Extension):
	def run(self):
				
		_ap = False

		# Get split_menu
		split = self.cfg.printv("split_menu")

		if split:
			# Should edit menu?
			if len(sys.argv) > 2:
				if sys.argv[2] == "sett":
					_ap = "gnome-settings.menu"
					ids = " ".join(sys.argv[3:])
				else:
					# Get ids
					ids = " ".join(sys.argv[2:])
			else:
				ids = ""

		def walk_menu(entry):
			if entry.get_type() == gmenu.TYPE_DIRECTORY and split and ids or entry.get_type() == gmenu.TYPE_DIRECTORY and not split:
				obj = "\n".join(map(walk_menu, entry.get_contents()))
				return core.menu(escape(entry.menu_id), escape(entry.name.replace("&","and")), obj, icon=entry.icon)
			elif entry.get_type() == gmenu.TYPE_DIRECTORY and split:
				if entry.menu_id in ("Administration","Preferences"):
					_id = "sett %s" % entry.menu_id
				else:
					_id = entry.menu_id
				
				return core.pipemenu(escape(entry.menu_id), escape(entry.name.replace("&","and")), "alan-show-extension %s %s" % (sys.argv[1], _id), icon=entry.icon)
			elif entry.get_type() == gmenu.TYPE_ENTRY and not entry.is_excluded:
				command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', entry.get_exec())
				if entry.launch_in_terminal:
					command = 'xterm -title "%s" -e %s' % \
						(entry.name.replace("&","and"), command)
				
				# New action
				act = ga.execute(escape(command))
				# Incorporate action in item
				item = core.item(escape(entry.name.replace("&","and")), act, icon=entry.icon)
				
				return item

		# Initiate pipemenu
		self.menu = struct.PipeMenu()
		self.menu.start() # add initial tag

		# Alias menu.insert() to i()
		i = self.menu.insert

		### Begin!

		# add things on APPLICATIONS MENU, see walk_menu.
		# Obtain applications menu.
		if not _ap:
			if os.path.exists("/etc/xdg/menus/applications.menu"):
				_ap = "applications.menu"
			else:
				_ap = "gnome-applications.menu"
		if split:
			path = "/" + ids
		else:
			path = "/"
		i("\n".join(map(walk_menu, gmenu.lookup_tree(_ap).get_directory_from_path(path).get_contents())))

		if not split or not ids:
			i(core.separator)

			# New menu, and on it map the Settings menu ;)
			if os.path.exists("/etc/xdg/menus/settings.menu"):
				_ap = "settings.menu"
			else:
				_ap = "gnome-settings.menu"
			i("\n".join(map(walk_menu, gmenu.lookup_tree(_ap).root.get_contents())))

		# Display info object
		#i(core.info(infos))

		# End
		self.menu.end()
