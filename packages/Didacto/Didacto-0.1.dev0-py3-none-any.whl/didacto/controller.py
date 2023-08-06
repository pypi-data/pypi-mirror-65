# -*- coding: utf-8 -*-

#   Didacto, un logiciel d'aide à l'organisation d'un corpus didactique
#   Copyright (C) 2020  Marco de Freitas
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.
#   If not, see <https://www.gnu.org/licenses/>.
#
#    contact:marco@sillage.ch

import io
import configparser
from view import *
from model import *


class Controller:
    def __init__(self):
        """Initialise the MVC structure."""
        prefs = self.open_saved_prefs()
        self.root = Tk()
        self.model = Model(prefs)
        self.view = View(self.root, self.model, self)

    def run(self):
        """Start windowing mechanism."""
        self.root.title("Didacto")
        self.root.deiconify()
        self.root.mainloop()

    def quit(self):
        """Quit programm."""
        self.root.destroy()

    def open_saved_prefs(self):
        """Opens preferences.ini file, return preferences keys and values."""
        config = configparser.ConfigParser()
        preferences = {}
        config.read('preferences.ini')
        for i in config['USER']:
            preferences[i] = config['USER'][i]
        return preferences

    def save_new_user_prefs(self, caca):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'path': '', 'separator':'', 'notation_format':'.ly'}
        config['USER']=caca
        with io.open('preferences.ini', 'w') as configfile:
            config.write(configfile)

# Code copié de:
# http://sametmax.com/ouvrir-un-fichier-avec-le-bon-programme-en-python/
    def run_file(self, path):
        """system call open file."""
        if not os.path.exists(path):  # Vérifier que le fichier existe
            raise IOError('No such file: %s' % path)

        if hasattr(os, 'access') and not os.access(path, os.R_OK):
            raise IOError('Cannot access file: %s' % path)

        # Lancer le bon programme pour le bon OS :

        if hasattr(os, 'startfile'):  # Windows
            # Startfile est très limité sous Windows,
            # on ne pourra pas savoir si il y a eu une erreur
            proc = os.startfile(path)
        elif sys.platform.startswith('linux'):  # Linux:
            proc = subprocess.Popen(['xdg-open', path],
                                    # on capture stdin et out pour
                                    # rendre le tout non bloquant
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        elif sys.platform == 'darwin':  # Mac:
            proc = subprocess.Popen(['open', '--', path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        else:
            raise NotImplementedError(
                "Your `%s` isn't a supported operatin system`." % sys.platform)

        # Proc sera toujours None sous Windows. Sous les autres OS,
        # il permet de récupérer le status code du programme, and
        # lire / ecrire sur stdin et out
        return proc
