# -*- coding: utf-8 -*-
#
# Alan: Semplice Menu Extension Framework
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team.
# Work released under the terms of the GNU GPL License, version 3 or later.
#
# This file cointain the appearance extension

import alan.core.structure as struct
import alan.core.objects.core as core
import alan.core.actions.glob as ga

import t9n.library as trans

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

wallpaperadd = core.item(_("Add"), ga.execute("nitrogen-add-wallpaper"), icon="gtk-add") # Item that opens nitrogen-add-wallpaper
wallpapermanage = core.item(_("Manage"), ga.execute("nitrogen"), icon="preferences-desktop-wallpaper") # Item that opens nitrogen
wallpapermenu = core.menu("wallmenu", _("Wallpaper"), "\n".join((wallpaperadd, wallpapermanage)), icon="preferences-desktop-wallpaper") # Menu that has on it wallpaperadd and wallpapermanage

themeselector = core.item(_("Appearance settings"), ga.execute("lxappearance"), icon="preferences-desktop-theme") # Theme selector

i(wallpapermenu)
i(themeselector)

# End
menu.end()
