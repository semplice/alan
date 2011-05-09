# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the actions library needed to insert actions into the pipe menu.

""" Here all global actions (http://openbox.org/wiki/Help:Actions#Global_actions) """

def execute(command, prompt=False, startupnotify=False):
	""" Runs a program.
	command = A string which is the command to be executed, along with any arguments to be passed to it. The "~" tilde character will be expanded to your home directory, but no other shell expansions or scripting syntax may be used in the command unless they are passed to the sh command. Also, the & character must be written as &amp; in order to be parsed correctly. <execute> is a deprecated name for <command>. 
	prompt = A string which Openbox will display in a popup dialog, along with "Yes" and "No" buttons. The execute action will only be run if you choose the "Yes" button in the dialog. (As of version 3.4.7) 
	startupnotify = A valid alan.actions.global.startupnotify object.
	"""
	
	if not prompt:
		# Make prompt ""
		prompt = ""
	else:
		# Make a correct prompt
		prompt = "<prompt>%s</prompt>" % prompt
	
	return """<action name="Execute">
	%s
	<command>%s</command>
</action> """ % (prompt, command.replace("&",""))


