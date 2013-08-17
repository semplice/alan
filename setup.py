#!/usr/bin/env python
# alan setup (using distutils)
# Copyright (C) 2011 Eugenio "g7" Paolantonio. All rights reserved.
# Work released under the GNU GPL license, version 3.

from distutils.core import setup

setup(name='alan',
      version='0.6.0',
      description='Openbox Menu Extension Framework',
      author='Eugenio Paolantonio and the Semplice Team',
      author_email='morarossa@gmail.com',
      url='http://launchpad.net/alan',
     # package_dir={'bin':''},
      scripts=['alan-gentree.py', 'alan-show-extension.py'],
      packages=['alan', 'alan.core', 'alan.core.actions', 'alan.core.objects', 'alan.ext'],
      data_files=[("/etc/alan", ["tree.conf"]),("/etc/xdg/menus", ["resources/semplice-applications.menu"])],
      requires=['ConfigParser', 'commands', 'gettext', 'gmenu', 'locale', 'os', 'sys', 're', 'shutil', 'xml.sax.saxutils', 't9n.library', 'hashlib'],
     )
