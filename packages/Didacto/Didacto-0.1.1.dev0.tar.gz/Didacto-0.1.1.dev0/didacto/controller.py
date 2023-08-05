# -*- coding: utf-8 -*-

#    Didacto, un logiciel d'aide à l'organisation d'un corpus didactique
#    Copyright (C) 2020  Marco de Freitas
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    contact:marco@sillage.ch

import configparser
from view import *
from model import *

class Controller:
    def __init__(self):
        prefs=self.set_prefs()
        self.root = Tk()
        self.model = Model(prefs)
        self.view = View(self.root, self.model,self)


    def run(self):
        #print(self.model.wordsDict)
        self.root.title("Didacto")
        self.root.deiconify()
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def set_prefs(self):
        config=configparser.ConfigParser()
        preferences={}
        config.read('preferences.ini')
        for i in config['USER']:
            preferences[i]=config['USER'][i]
        return preferences
        


#Code copié de http://sametmax.com/ouvrir-un-fichier-avec-le-bon-programme-en-python/


    def run_file(self,path):
     
        # Pas de EAFP cette fois puisqu'on est dans un process externe,
        # on ne peut pas gérer l'exception aussi facilement, donc on fait
        # des checks essentiels avant.
     
        # Vérifier que le fichier existe
        if not os.path.exists(path):
            raise IOError('No such file: %s' % path)
     
        # On a accès en lecture ?
        if hasattr(os, 'access') and not os.access(path, os.R_OK):
            raise IOError('Cannot access file: %s' % path)
     
        # Lancer le bon programme pour le bon OS :
     
        if hasattr(os, 'startfile'): # Windows
            # Startfile est très limité sous Windows, on ne pourra pas savoir
            # si il y a eu une erreu
            proc = os.startfile(path)
     
        elif sys.platform.startswith('linux'): # Linux:
            proc = subprocess.Popen(['xdg-open', path], 
                                     # on capture stdin et out pour rendre le 
                                     # tout non bloquant
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     
        elif sys.platform == 'darwin': # Mac:
            proc = subprocess.Popen(['open', '--', path], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     
        else:
            raise NotImplementedError(
                "Your `%s` isn't a supported operatin system`." % sys.platform)
     
        # Proc sera toujours None sous Windows. Sous les autres OS, il permet de
        # récupérer le status code du programme, and lire / ecrire sur stdin et out
        return proc

