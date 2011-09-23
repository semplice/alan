# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 2.
#
# This file cointain the music extension

#### BASED ON http://david.chalkskeletons.com/scripts/ob-mpd-0.3.py
#
# Author: John McKnight <jmcknight@gmail.com>
# License: GPL 2.0
#
####

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga
import t9n.library as trans

import alan.core.extension

import mpd
import os, sys

_ = trans.translation_init("alan")


executable = " ".join(sys.argv)

# Informations about extension ;)
coders = { "John McKnight (original mpd extension)":"mailto:jmcknight@gmail.com", "Eugenio Paolantonio":"http://blog.medesimo.eu" }
infos = {_("Coders"):coders}

class MPD:
	def __init__(self):
		""" This class rapresents a MPD extension. """
		
		self.NAME = "MPD"
		
		# Assume port is 6600
		mpdPort = 6600
		
		# Connect to database
		self.client = mpd.MPDClient()
		self.client.connect("localhost", mpdPort)
		self.song = self.client.currentsong()
		self.stats = self.client.stats()
		self.status = self.client.status()
		
		#print self.song
				
	def play(self):
		""" Starts playing """
		
		self.client.play()

	def pause(self):
		""" Pauses! """
		
		self.client.pause()

	def stop(self):
		""" Stops the music player. """
		
		self.client.stop()

	def prev(self):
		""" Previous song """
		
		self.client.previous()


	def next(self):
		""" Next song """
		
		self.client.next()
	
	def return_album_songs(self, album):
		""" Returns a list of items that changes the song. """
		
		sngs = []
		for song in self.client.listallinfo():
			try:
				if song['album'] == album:
					# Yay!
					sngs.append(core.item(song["title"], ga.execute(executable + " %s changesong %s %s %s" % (self.NAME, song["title"], song["album"], song["artist"]))))
			except:
				pass
		
		return sngs
	
	def return_author_albums(self, artist):
		""" Returns a list of submenus that uses return_album_songs """
		
		albums = []
		num = 0
		for song in self.client.listallinfo():
			try:
				if song["artist"] == artist:
					# Yay!
					num += 1
					if not song["album"] in albums: albums.append(song["album"])
			except:
				pass
		
		albums_all = []
		num = 0
		for album in albums:
			num += 1
			try: albums_all.append(core.menu("albumsub%s" % num, album, "\n".join(self.return_album_songs(album))))
			except: pass
		
		return albums_all
		

class Extension(alan.core.extension.Extension):

	def run(self):
		# Initiate pipemenu
		self.menu = struct.PipeMenu()
		self.menu.start() # add initial tag

		# Alias menu.insert() to i()
		i = self.menu.insert

		### Begin!

		# We should determine which player use, but hey, currently only MPD is supported :)
		PLAYERS = (MPD,)

		# Process player
		for player in PLAYERS:

			# Declare class
			clas = player()

			if len(sys.argv) > 3:
				# Called from an already made pipe menu
				if clas.NAME == sys.argv[2]:
					if sys.argv[3] == "play": clas.play()
					if sys.argv[3] == "pause": clas.pause()
					if sys.argv[3] == "stop": clas.stop()
					if sys.argv[3] == "restartsong": clas.restartsong()
					if sys.argv[3] == "prev": clas.prev()
					if sys.argv[3] == "next": clas.next()
				sys.exit(0)
			
			#######
			# A simple ASCII mockup :D
			#
			# Play (If we are paused or stopped) - If we are playing, show Pause instead of Play.
			# Stop (If we are playing or pausing)
			# ----
			# <Song Name> -> Click -> Restarts song
			# <Album> -> Submenu that shows all songs in the album
			# <Author> -> Submenu that shows all albums and then songs in them
			# ----
			# Previous
			# Next
			# ----
			# Info
			#######
			
			# Begin creating all needed objects
			play = core.item(_("Play"), ga.execute(executable + " %s play" % clas.NAME))
			pause = core.item(_("Pause"), ga.execute(executable + " %s pause" % clas.NAME))
			stop = core.item(_("Stop"), ga.execute(executable + " %s stop" % clas.NAME))
			
			if clas.status["state"] == "stop" or not clas.song["title"]:
				song = _("Play a random song")
				album = False
				author = False
			else:
				song = clas.song["title"]
				#album = core.menu()
				#print clas.song["album"]
				try: album = core.menu("albumsub", clas.song["album"], "\n".join(clas.return_album_songs(clas.song["album"])))
				except: album = False
				
				try: author = core.menu("artistsub", clas.song["artist"], "\n".join(clas.return_author_albums(clas.song["artist"])))
				except: author = False
			
			song = core.item(_(song), ga.execute(executable + " %s restartsong" % clas.NAME))
			
			prev = core.item(_("Previous"), ga.execute(executable + " %s prev" % clas.NAME))
			next = core.item(_("Next"), ga.execute(executable + " %s next" % clas.NAME))
			
			# Begin adding to menu
			i(core.header(clas.NAME))
			
			if clas.status["state"] == "stop" or clas.status["state"] == "pause": i(play)
			if clas.status["state"] == "play": i(pause)
			if clas.status["state"] == "play" or clas.status["state"] == "pause": i(stop)
			
			# Separator
			i(core.separator)
			
			# Song name
			i(song)
			if album: i(album)
			if author: i(author)

			
			# Previus/Next
			if clas.status["state"] in ("play", "pause"):
				# Separator
				i(core.separator)
				
				i(prev)
				i(next)
			
		# Display info object
		i(core.info(infos))

		# End
		self.menu.end()
