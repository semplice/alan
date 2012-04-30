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

userbegin = 1000

HOME = os.getenv("HOME")
USER = os.getenv("USER")

cfile = os.path.join(HOME, ".semplice-logout")

_ = trans.translation_init("alan")

# Informations about extension ;)
coders = { "Eugenio Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

class Extension(alan.core.extension.Extension):
	def run(self):

		# Initiate pipemenu
		self.menu = struct.PipeMenu(use_cache=self.cfg.printv("use_cache","Alan"), cache="logout", cache_trigger=(self.cfg.path, cfile, "/etc/passwd"))
		if self.menu.cache_check():
			self.menu.cache_read()
		else:
			self.menu.start() # add initial tag

			# Alias menu.insert() to i()
			i = self.menu.insert

			### Begin!

			sort = ("lock", "logout", "switch", "suspend", "hibernate", "shutdown", "reboot") # Workaround that has to be made after switching from numbers to words.
			
			actions = {"lock":_("Lock Screen"), "logout":_("Logout"), "switch":_("Switch User"), "switch_guest":_("Guest session"), "suspend":_("Suspend"), "hibernate":_("Hibernate"), "shutdown":_("Shutdown"), "reboot":_("Reboot")}
			ections = {"lock":"semplice-logout --lock", "logout":"semplice-logout --logout", "switch":"semplice-logout --switch-user", "switch_guest":"semplice-logout --switch-to-guest", "suspend":"semplice-logout --suspend", "hibernate":"semplice-logout --hibernate", "shutdown":"semplice-logout --shutdown","reboot":"semplice-logout --reboot"}
			ictions = {"lock":"system-lock-screen", "logout":"system-log-out", "switch":"system-users", "switch_guest":"system-users", "suspend":"gnome-session-suspend", "hibernate":"gnome-session-hibernate", "shutdown":"gnome-session-halt", "reboot":"gnome-session-reboot"}

			# After <robo>, add a separator.
			sep = ("switch", "hibernate")

			# Read configuration file
			if os.path.exists(cfile):
				cfg = cp.SafeConfigParser()
				cfg.read(cfile)
				
				# Get last choice
				last = cfg.get("Last","last_action")
				if last.lower() == "none": last = False
			else:
				last = False

			# Add that choice!
			if last:
				choice = actions[last] + " " + _("(CTRL+ALT+SPACE)")
				i(core.item(choice, ga.execute(ections[last]), icon=ictions[last]))
				i(core.separator)

			# Add normal choices
			
			# Lock screen
			i(core.item(_("Lock Screen"), ga.execute("semplice-logout --lock"), icon="system-lock-screen"))
			
			# Logout
			i(core.item(_("Logout"), ga.execute("semplice-logout --logout"), icon="system-log-out"))
			
			# Switch User
			# create menu:
			switch_items = []
			# open passwd and populate switch_items
			with open("/etc/passwd", "r") as passwd:
				for line in passwd.readlines():
					line = line.split(":")
					_uid = int(line[2])
					if _uid < userbegin or _uid == 65534:
						continue # Skip users < userbegin and 65534 (nobody)
					
					_uname = line[0]
					_udesc = line[4].split(",")[0]
					if not _udesc: _udesc = _uname
					
					if not _uname == USER:
						_uhome = line[5]
						if os.path.exists(os.path.join(_uhome, ".face")):
							_uface = os.path.join(_uhome, ".face")
						else:
							_uface = "system-users"
						
						switch_items.append(core.item(_udesc, ga.execute("semplice-logout --switch-to %s" % _uname), icon=_uface))
					else:
						_uface = "gnome-settings-default-applications"
					
						# create another menu on which put the "change profile image" item...
						change_image = core.item(_("Change profile image"), ga.execute("semplice-change-face"), icon="eog")
						switch_items.append(core.menu("usermenu", _udesc, change_image, icon=_uface))
					
			# add guest session
			switch_items.append(core.separator)
			#switch_items.append(core.item(_("Guest session"), ga.execute("semplice-logout --switch-to-guest"), icon="system-users"))
			# add Other...
			switch_items.append(core.item(_("Other..."), ga.execute("semplice-logout --switch-user"), icon="gdm"))
			
			# then create the menu...
			i(core.menu("switchmenu", _("Switch User"), "\n".join(switch_items), icon="system-users"))
			
			# Separator
			i(core.separator)
			
			# Suspend
			i(core.item(_("Suspend"), ga.execute("semplice-logout --suspend"), icon="gnome-session-suspend"))
			
			# Hibernate
			i(core.item(_("Hibernate"), ga.execute("semplice-logout --hibernate"), icon="gnome-session-hibernate"))
			
			# Separator
			i(core.separator)
			
			# Shutdown
			i(core.item(_("Shutdown"), ga.execute("semplice-logout --shutdown"), icon="gnome-session-halt"))
			
			# Reboot
			i(core.item(_("Reboot"), ga.execute("semplice-logout --reboot"), icon="gnome-session-reboot"))
			
			#for num in sort:
			#	robo = actions[num]
			#	i(core.item(robo, ga.execute(ections[num]), icon=ictions[num]))
			#	if num in sep:
			#		# We should add a separator!
			#		i(core.separator)

			# Add Settings... item
			i(core.separator)
			i(core.item(_("Settings..."), ga.execute("semplice-logout --settings"), icon="preferences-desktop"))

			# End
			self.menu.end()
