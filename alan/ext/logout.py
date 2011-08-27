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

import os, sys

import t9n.library as trans

HOME = os.getenv("HOME")

_ = trans.translation_init("alan")

# Informations about extension ;)
coders = { "Eugenio Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

# Initiate pipemenu
menu = struct.PipeMenu()
menu.start() # add initial tag

# Alias menu.insert() to i()
i = menu.insert

### Begin!

actions = {0:_("Lock Screen"), 1:_("Logout"), 2:_("Switch User"), 3:_("Suspend"), 4:_("Hibernate"), 5:_("Shutdown"), 6:_("Reboot")}
ections = {0:"semplice-logout --lock", 1:"semplice-logout --logout", 2:"semplice-logout --switch-user", 3:"semplice-logout --suspend", 4:"semplice-logout --hibernate", 5:"semplice-logout --shutdown",6:"semplice-logout --reboot"}
ictions = {0:"system-lock-screen", 1:"system-log-out", 2:"system-users", 3:"gnome-session-suspend", 4:"gnome-session-hibernate", 5:"gnome-session-halt", 6:"gnome-session-reboot"}

# After <num>, add a separator.
sep = (2, 4)

# If ~/.lastlogoutchoice exists; read that and make that choice first.
_file = os.path.join(HOME, ".lastlogoutchoice")
# But if .lastlogoutchoice.lock exists, read that instead.
if os.path.exists(os.path.join(HOME, ".lastlogoutchoice.lock")): _file = os.path.join(HOME, ".lastlogoutchoice.lock")
if os.path.exists(_file):
	with open(_file) as f:
		last = f.readline().replace("\n","")
else:
	last = False

# Add that choice!
if last:
	choice = actions[int(last)] + " (CTRL+ALT+SPACE)"
	i(core.item(choice, ga.execute(ections[int(last)]), icon=ictions[int(last)]))
	i(core.separator())

# Add normal choices
for num, robo in actions.iteritems():
	i(core.item(robo, ga.execute(ections[num]), icon=ictions[num]))
	if num in sep:
		# We should add a separator!
		i(core.separator())

# End
menu.end()
