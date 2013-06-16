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

# Informations about extension ;)
coders = { "Eugenio Paolantonio":"http://blog.medesimo.eu" }
infos = {"Coders":coders}

class Extension(alan.core.extension.Extension):
	def exfm(self, filemanager, path):
		return "%s \"%s\"" % (filemanager, path)
	
	def run(self):
		
		# Get filemanager
		filemanager = self.cfg.printv("filemanager")
		if not filemanager: filemanager = "pcmanfm --new-win" # Default to pcmanfm if not filemanager specified.
		
		# Initiate pipemenu
		self.menu = struct.PipeMenu(use_cache=self.cfg.printv("use_cache","Alan"), cache="places", cache_trigger=(self.cfg.path, os.path.join(HOME,".gtk-bookmarks"), "/proc/mounts"))
		if self.menu.cache_check():
			self.menu.cache_read() # Read cache
		else:
			self.menu.start() # add initial tag

			# Alias menu.insert() to i()
			i = self.menu.insert

			### Begin!

			# Home
			i(core.item(USER, ga.execute(self.exfm(filemanager, "file://%s" % HOME)), icon="user-home"))

			# Desktop
			i(core.item(_("Desktop"), ga.execute(self.exfm(filemanager, "file://%s" % os.path.join(HOME,"Desktop"))), icon="user-desktop"))

			# Trash
			i(core.item(_("Trash"), ga.execute(self.exfm(filemanager, "trash://")), icon="user-trash"))

			# Computer
			i(core.item(_("Computer"), ga.execute(self.exfm(filemanager, "computer://")), icon="computer"))

			i(core.separator)

			#### MOUNTED ITEMS

			# Root (/)
			i(core.item(_("System (/)"), ga.execute(self.exfm(filemanager, "file:///")), icon="drive-harddisk"))

			with open("/proc/mounts") as mounts:

				# Other items listed in /media
				for media in mounts.readlines():
					if "/media" in media:
						
						if ICONS:
							if "iso9660" in media or "udf" in media:
								# It is a CD. Maybe.
								icon = "media-optical"
							else:
								icon = "drive-harddisk"
						else:
							icon = ""
						
						# Is on media. Yay.
						dire = media.split(" ")[1].replace('\\040'," ") # use only the directory name
						i(core.item(os.path.basename(dire).replace("_","__"), ga.execute(self.exfm(filemanager, dire)), icon=icon))

			if os.path.exists(os.path.join(HOME, ".gtk-bookmarks")):
				i(core.separator)

				_file = open(os.path.join(HOME, ".gtk-bookmarks"))
				lines = _file.readlines()
				for line in lines:
					line = line.split(" ")
					directory = line[0].replace("\n","")
					if len(line) > 1:
						name = " ".join(line[1:]).replace("_","__").replace("\n","")
					else:
						name = os.path.basename(directory.replace("file://","")).replace("_","__").replace("\n","")
					if directory.startswith("smb://"):
						icon = "folder-remote-smb"
					elif directory.startswith("nfs://"):
						icon = "folder-remote-nfs"
					elif directory.startswith("ssh://"):
						icon = "folder-remote-ssh"
					elif directory.startswith("ftp://"):
						icon = "folder-remote-ftp"
					else:
						icon = "folder"
					i(core.item(name, ga.execute(self.exfm(filemanager, directory)), icon=icon))

			# End
			self.menu.end()
