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
import glob

import gmenu, re, sys
from xml.sax.saxutils import escape

# Informations about extension ;)
coders = { "Luke Macken (xdg-menu.py)":"mailto:lmacken@redhat.com", "Miroslav Lichvar (xdg-menu.py)":"mailto:mlichvar@redhat.com", "Eugenio \"g7\" Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

class Extension(alan.core.extension.Extension):
	def run(self):
				
		ids = ""

		# Get split_menu
		split = self.cfg.printv("split_menu")
		
		# Get hide_settings_menus
		hide_settings_menus = self.cfg.printv("hide_settings_menus")

		if split:
			# Should edit menu?
			if len(sys.argv) > 2:
					ids = " ".join(sys.argv[2:])
		
		if hide_settings_menus:
			# Should hide menus?
			to_skip = ()
		else:
			to_skip = ("Administration", "Preferences")

		# Lookup menu file
		if os.path.exists("/etc/xdg/menus/semplice-applications.menu"):
			applications_menu = "semplice-applications.menu"
		elif os.path.exists("/etc/xdg/menus/gnome-applications.menu"):
			applications_menu = "gnome-applications.menu"
		else:
			applications_menu = "applications.menu" # Force to applications.menu, may fail if not existent, of course.

		def walk_menu_system(entry):
			return walk_menu(entry, is_system=True)

		def walk_menu(entry, is_system=False):
			if entry.get_type() == gmenu.TYPE_DIRECTORY and split and ids or entry.get_type() == gmenu.TYPE_DIRECTORY and not split:
								
				if not entry.menu_id in to_skip:
					obj = "\n".join(map(walk_menu, entry.get_contents()))
				elif is_system:
					obj = "\n".join(map(walk_menu_system, entry.get_contents()))
				else:
					return ""
				
				return core.menu(escape(entry.menu_id), escape(entry.name.replace("&","and")), obj, icon=entry.icon)
			elif entry.get_type() == gmenu.TYPE_DIRECTORY and split:
				if not entry.menu_id in to_skip:
					return core.pipemenu(escape(entry.menu_id), escape(entry.name.replace("&","and")), "alan-show-extension %s %s" % (sys.argv[1], entry.menu_id), icon=entry.icon)
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
		#self.menu = struct.PipeMenu(use_cache=self.cfg.printv("use_cache","Alan"), cache="xdgmenu", cache_trigger=(self.cfg.path, glob.glob("/usr/share/applications/desktop.*.cache")[0]))
		self.menu = struct.PipeMenu()
		if self.menu.cache_check():
			# Read cache
			self.menu.cache_read()
		else:
			self.menu.start() # add initial tag

			# Alias menu.insert() to i()
			i = self.menu.insert

			### Begin!

			if split:
				path = "/" + ids
			else:
				path = "/"
			i("\n".join(map(walk_menu, gmenu.lookup_tree(applications_menu).get_directory_from_path(path).get_contents())))

			#### SYSTEM SETTINGS
			if not ids and not hide_settings_menus:
				i(core.separator)

				# Prefs
				prefs = gmenu.lookup_tree(applications_menu).get_directory_from_path("/System/Preferences")
				if not split:
					prefs_items = "\n".join(map(walk_menu_system, prefs.get_contents()))
					i(core.menu(escape(prefs.menu_id), escape(prefs.name.replace("&","and")), prefs_items, icon=prefs.icon))
				else:
					i(core.pipemenu(escape(prefs.menu_id), escape(prefs.name.replace("&","and")), "alan-show-extension %s %s" % (sys.argv[1], "System/Preferences"), icon=prefs.icon))
				
				# Admin
				admin = gmenu.lookup_tree(applications_menu).get_directory_from_path("/System/Administration")
				if not split:
					admin_items = "\n".join(map(walk_menu_system, admin.get_contents()))
					i(core.menu(escape(admin.menu_id), escape(admin.name.replace("&","and")), admin_items, icon=admin.icon))
				else:
					i(core.pipemenu(escape(admin.menu_id), escape(admin.name.replace("&","and")), "alan-show-extension %s %s" % (sys.argv[1], "System/Administration"), icon=admin.icon))

			# Display info object
			#i(core.info(infos))

			# End
			self.menu.end()
