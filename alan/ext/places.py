# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the places extension

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga

import alan.core.extension

import t9n.library as trans

import os, sys, commands

HOME = os.getenv("HOME")
USER = os.getenv("USER")

ICONS = os.getenv("ALANICONS")

_ = trans.translation_init("alan")

def exfm(path):
	return "pcmanfm \"%s\"" % path

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

		# Home
		i(core.item(USER, ga.execute(exfm("file://%s" % HOME)), icon="user-home"))

		# Desktop
		i(core.item(_("Desktop"), ga.execute(exfm("file://%s" % os.path.join(HOME,"Desktop"))), icon="user-desktop"))

		# Trash
		i(core.item(_("Trash"), ga.execute(exfm("trash://")), icon="user-trash"))

		# Computer
		i(core.item(_("Computer"), ga.execute(exfm("computer://")), icon="computer"))

		i(core.separator)

		#### MOUNTED ITEMS

		# Root (/)
		i(core.item(_("System (/)"), ga.execute(exfm("file:///")), icon="drive-harddisk"))

		with open("/proc/mounts") as mounts:

			# Other items listed in /media
			for media in mounts.readlines():
				if "/media" in media:
					
					if ICONS:
						if "iso9660" in media:
							# It is a CD. Maybe.
							icon = "media-optical"
						else:
							icon = "drive-harddisk"
					else:
						icon = ""
					
					# Is on media. Yay.
					dire = media.split(" ")[1].replace('\\040'," ") # use only the directory name
					i(core.item(os.path.basename(dire).replace("_","__"), ga.execute(exfm(dire)), icon=icon))

		if os.path.exists(os.path.join(HOME, ".gtk-bookmarks")):
			i(core.separator)

			_file = open(os.path.join(HOME, ".gtk-bookmarks"))
			lines = _file.readlines()
			for line in lines:
				line = line.split(" ")
				directory = line[0]
				name = " ".join(line[1:]).replace("_","__")
				i(core.item(name, ga.execute(exfm(directory)), icon="folder"))

		# End
		self.menu.end()
