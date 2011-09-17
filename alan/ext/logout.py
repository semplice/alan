# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the logout extension

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga

import alan.core.extension

import os, sys
import ConfigParser as cp

import t9n.library as trans

HOME = os.getenv("HOME")

cfile = os.path.join(HOME, ".semplice-logout")

_ = trans.translation_init("alan")

# Informations about extension ;)
coders = { "Eugenio Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

class Extension(alan.core.extension.Extension):
	def run(self):

		# Initiate pipemenu
		self.menu = struct.PipeMenu()
		self.menu.start() # add initial tag

		# Alias menu.insert() to i()
		i = self.menu.insert

		### Begin!

		sort = ("lock", "logout", "switch", "suspend", "hibernate", "shutdown", "reboot") # Workaround that has to be made after switching from numbers to words.
		
		actions = {"lock":_("Lock Screen"), "logout":_("Logout"), "switch":_("Switch User"), "suspend":_("Suspend"), "hibernate":_("Hibernate"), "shutdown":_("Shutdown"), "reboot":_("Reboot")}
		ections = {"lock":"semplice-logout --lock", "logout":"semplice-logout --logout", "switch":"semplice-logout --switch-user", "suspend":"semplice-logout --suspend", "hibernate":"semplice-logout --hibernate", "shutdown":"semplice-logout --shutdown","reboot":"semplice-logout --reboot"}
		ictions = {"lock":"system-lock-screen", "logout":"system-log-out", "switch":"system-users", "suspend":"gnome-session-suspend", "hibernate":"gnome-session-hibernate", "shutdown":"gnome-session-halt", "reboot":"gnome-session-reboot"}

		# After <robo>, add a separator.
		sep = ("switch", "hibernate")

		# Read configuration file
		if os.path.exists(cfile):
			cfg = cp.SafeConfigParser()
			cfg.read(cfile)
			
			# Get last choice
			last = cfg.get("Last","last_action")
			if not last: last = False
		else:
			last = False

		# Add that choice!
		if last:
			choice = actions[last] + _(" (CTRL+ALT+SPACE)")
			i(core.item(choice, ga.execute(ections[last]), icon=ictions[last]))
			i(core.separator)

		# Add normal choices
		for num in sort:
			robo = actions[num]
			i(core.item(robo, ga.execute(ections[num]), icon=ictions[num]))
			if num in sep:
				# We should add a separator!
				i(core.separator)

		# Add Settings... item
		i(core.separator)
		i(core.item(_("Settings..."), ga.execute("semplice-logout --settings"), icon="preferences-desktop"))

		# End
		self.menu.end()
