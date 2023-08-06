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

from os import *

from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import ttk
from tkinter import *


class Tree():
    """Class for treeview specific functions"""
    def __init__(self, root):
        pass


class View():
    def __init__(self, root, model, controller):
        """Initialize the main window"""
        self.model = model
        self.root = root
        self.controller = controller
        self.pref_win_statut = False
        self.help_win_statut = False
        self.about_win_statut = False
        # contrôle l'état des fenêtre uniques (aide, à propos, préférences)
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Choisir Dossier',
                                  accelerator='ctrl+p',
                                  command=self.choose_folder)
        self.filemenu.add_command(label='Rafraîchir',
                                  accelerator='ctrl+r',
                                  command=self.tree_refresh)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Préférences',
                                  command=self.create_preferences_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quiter',
                                  accelerator='ctrl+q',
                                  command=self.controller.quit)
        self.menubar.add_cascade(label='Fichier', menu=self.filemenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='Aide',
                                  command=self.create_help_window)
        self.helpmenu.add_command(label='A propos',
                                  command=self.create_about_window)
        self.menubar.add_cascade(label='Aide', menu=self.helpmenu)
        self.root.bind('<Control-p>', self.select_folder)
        self.root.bind('<Control-r>', self.refresh_treeview)
        self.root.bind('<Control-q>', self.close_programm)
        self.root.config(menu=self.menubar)
        self.frame0 = Frame(root)
        self.frame0.text = StringVar('')
        l1 = Label(self.frame0, textvariable=self.frame0.text)
        l1.pack()

        self.frame0.pack()
        self.checkbox_value = BooleanVar()
        checkbox = Checkbutton(root,
                               text="Inclure sous-dossiers",
                               variable=self.checkbox_value,
                               command=self.do_nothing)
        checkbox.pack()
        self.frame1 = Frame(root)

        self.buttonChoose = Button(root,
                                   text='Choisir dossier',
                                   command=self.choose_folder)
        self.buttonRefresh = Button(root,
                                    text='Rafraîchir',
                                    command=self.tree_refresh)
        self.tv = ttk.Treeview(root,
                               columns=['files', 'path'],
                               selectmode='browse')
        self.tv.column('#0', minwidth=100, stretch=True)
        self.tv.column('files', minwidth=250, stretch=True)
        self.tv.column('path', minwidth=250, stretch=True)
        self.tv.heading('#0', text='Mots-clef')
        self.tv.heading('files', text='Fichiers', anchor='center')
        self.tv.heading('path', text='Chemin', anchor='center')
        self.tv.pack(expand=True, fill='both')
        self.yscroll = Scrollbar(root,
                                 orient='vertical',
                                 command=self.tv.yview)
        self.yscroll.pack(side='right', fill='y')

        self.collapsebox_value = BooleanVar()
        collapsebox = Checkbutton(root,
                                  text="Ouvrir/Fermer tout",
                                  variable=self.collapsebox_value,
                                  command=lambda:
                                       self.collapse_nodes(
                                           self.collapsebox_value.get()))
        collapsebox.pack(side=TOP)

        for widget in [self.buttonChoose,
                       self.buttonRefresh,
                       self.tv,
                       self.yscroll]:
            widget.pack(side=LEFT)

        self.frame1.pack()
        self.tv.bind('<<TreeviewSelect>>', self.prout)
        self.tv.bind('<<TreeviewOpen>>', self.prouti)
        self.tv.bind('<<TreeviewClose>>', self.prouta)
        self.tv.bind("<Double-1>", self.on_double_click)
        self.tv.bind("<ButtonRelease-3>", self.on_right_click)

        self.get_saved_prefs()
        self.tree_initialise()
        


    def get_saved_prefs(self):
        """This function recalls prefs stored values"""
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path=self.prefs['path']
        self.prefs_separator=self.prefs['separator']
        self.prefs_notation=self.prefs['notation_format']
        

    def tree_initialise(self):
        """This function init tree data and displays it"""
        if self.prefs_path == '':
            pass
        else:
            self.frame0.text.set(self.prefs_path)
            self.get_saved_prefs()
            self.tree_refresh()
            

    def collapse_nodes(self, value):
        """Treview function, collapse/open all nodes"""
        for tree_index in range(len(self.model.wordsDict)):
            self.tv.item(tree_index, open=value)


# Cette fonction efface le contenu de l'arbre
    def tree_delete(self, size):
            if size > 0:
                for idid in range(size):
                    self.tv.delete(idid)

# Cette fonction recrée un arbre à partir du dictionnaire
    def tree_repopulate(self):
            tree_index = 0
            for key in self.model.wordsDict:
                self.tv.insert('',
                               index=tree_index,
                               iid=tree_index,
                               text=key,
                               values=[''])
                for list_index in range(len(self.model.wordsDict[key])):
                    self.tv.insert(tree_index,
                                   index=tree_index,
                                   text='',
                                   values=[self.model.wordsDict[key][list_index]['name'],
                                           self.model.wordsDict[key][list_index]['path']])
                tree_index += 1

    def tree_refresh(self):  # oh copie dself.get_saved_prefs()e code de choose_folder
        treeSize = len(self.model.wordsDict)
        path = self.frame0.text.get()
        recursive = self.checkbox_value.get()
        self.model.scan_repertory(path, recursive)
        self.tree_delete(treeSize)
        self.tree_repopulate()
        
# fontions de la fenêtre principale
    def get_directory(self):
            givenPath = filedialog.askdirectory()
            if givenPath is not None:
                return givenPath

    def choose_folder(self):
        treeSize = len(self.model.wordsDict)
        newPath = self.get_directory()
        self.frame0.text.set(newPath)
        recursive = self.checkbox_value.get()
        self.model.scan_repertory(newPath, recursive)
        self.tree_delete(treeSize)
        self.tree_repopulate()

# gestion des racourcis clavier
    def select_folder(self, event):
        """Command function for keyboard shortcuts, calls path selection function."""
        self.choose_folder()

    def refresh_treeview(self, event):
        """Command function for keyboard shortcuts, calls treeview refresh function."""
        self.tree_refresh()

    def close_programm(self, event):
        """Command function for keyboard shortcuts, calls programm quit function."""
        self.controller.quit()

# Test sur la sélection par la souris
    def prout(self, event):
        """This funtion """
        print("selected:" + self.tv.focus())

    def prouti(self, caca):
        print("Open")

    def prouta(self, caca):
        print("Close")

# Gestion de la souris
    def on_double_click(self, event):
        """Function called by Mouse double click, calls open pdf file function."""
        item = self.tv.identify("item", event.x, event.y)
        self.controller.run_file(self.tv.item(item)["values"][1])

    def on_right_click(self, event):
        """Function called by mouse right click, calls opend notation file function."""
        item = self.tv.identify("item", event.x, event.y)
        path = self.tv.item(item)["values"][1][:-4]+'.ly'
        self.controller.run_file(path)

# création des sous-fenêtres 
    def create_about_window(self):
        """About Window Creation.Singleton mecanism"""
        if self.about_win_statut is False:
            self.about_win_statut = True
            about_window = AboutWindow(self.root)

    def create_help_window(self):
        """Help Window Creation"""
        if self.help_win_statut is False:
            self.help_win_statut is True
            help_window = HelpWindow(self.root)

    def create_preferences_window(self):
        """User preferences window creation"""
        if self.pref_win_statut is False:
            self.pref_win_statut = True
            self.prefs = PreferencesWindow(self.root, self.controller, self)

    def do_nothing(self):
        """This functino does nothing. Used as Default value for a new widget command function."""
        pass


class Menubar():
    def __init(self, arg):
        self.root = arg
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Choisir Dossier',
                                  accelerator='ctrl+p',
                                  command=self.choose_folder)
        self.filemenu.add_command(label='Rafraîchir',
                                  accelerator='ctrl+r',
                                  command=self.tree_refresh)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quiter',
                                  accelerator='ctrl+q',
                                  command=self.controller.quit)
        self.menubar.add_cascade(label='Fichier', menu=self.filemenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='Aide',
                                  command=self.create_help_window)
        self.helpmenu.add_command(label='A propos',
                                  command=self.create_about_window)
        self.menubar.add_cascade(label='Aide', menu=self.helpmenu)
        self.root.bind('<Control-p>', self.select_folder)
        self.root.bind('<Control-r>', self.refresh_treeview)
        self.root.bind('<Control-q>', self.close_programm)
        self.root.config(menu=self.menubar)


class PreferencesWindow():
    def __init__(self, root, controller, view):
        self.root = root
        self.controller = controller
        self.view = view
        self.preferences_window = Toplevel(self.root)
        self.preferences_window.wm_title("Préférences")
       
        self.buttonChooseDefaultPath = Button(
                            self.preferences_window,
                            text='Choisir un dossier a indexer par défaut',
                            command=self.choose_default)

        self.buttonChooseDefaultPath.pack()
        self.path_label = StringVar()

        self.l1 = Label(self.preferences_window,
                        textvariable=self.path_label)
        self.l1.pack()
        self.l2 = Label(self.preferences_window,
                       text="Séparateur par défaut")
        self.l2.pack()
        self.separator = StringVar()
        self.R1 = Radiobutton(self.preferences_window,
                         text="espace",
                         variable=self.separator,
                         value=" ",
                         command=lambda: self.set_temp_prefs('', None))
        self.R1.pack(anchor=CENTER)
        self.R2 = Radiobutton(self.preferences_window,
                         text="virgule",
                         variable=self.separator,
                         value=",",
                         command=lambda: self.set_temp_prefs(',', None))
        self.R2.pack(anchor=CENTER)
        self.l3 = Label(self.preferences_window,
                       text="Format des fichiers de notation")
        self.l3.pack()
        self.notation_format = StringVar()
        self.R3 = Radiobutton(self.preferences_window,
                         text="Lylipond",
                         variable=self.notation_format,
                         value=".ly ",
                         command=lambda: self.set_temp_prefs(None, '.ly'))
        self.R3.pack(anchor=CENTER)
        self.R4 = Radiobutton(self.preferences_window,
                         text="Musescore",
                         variable=self.notation_format,
                         value=".mscz",
                         command=lambda: self.set_temp_prefs(None, '.mscz'))
        self.R4.pack(anchor=CENTER)
        self.R5 = Radiobutton(self.preferences_window,
                         text="Sibélius",
                         variable=self.notation_format,
                         value=".sib",
                         command=lambda: self.set_temp_prefs(None, '.sib'))
        self.R5.pack(anchor=CENTER)
        self.R6 = Radiobutton(self.preferences_window,
                         text="Finale",
                         variable=self.notation_format,
                         value=".musx",
                         command=lambda: self.set_temp_prefs(None, '.musx'))
        self.R6.pack(anchor=CENTER)
        self.buttonResetPreferences = Button(self.preferences_window,
                                             text='Rétablir valeurs par défaut',
                                             command=self.reset_prefs)
        self.buttonResetPreferences.pack(side=RIGHT)
        self.buttonDiscardPreferences = Button(self.preferences_window,
                                               text='Annuler',
                                               command=self.close_prefs)
        self.buttonDiscardPreferences.pack(side=RIGHT)
        self.buttonSavePreferences = Button(self.preferences_window,
                                            text='Sauvegarder',
                                            command=self.save_temp_prefs)
        self.buttonSavePreferences.pack(side=RIGHT)
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path=self.prefs['path']
        self.prefs_separator=self.prefs['separator']
        self.prefs_notation=self.prefs['notation_format']
        self.display_saved_prefs()
        self.path_label.set(self.prefs_path)
        self.invoke_prefs()

    def get_saved_prefs(self):
        """This function recalls stored values"""
        self.prefs=self.controller.open_saved_prefs()
        self.prefs_path=self.prefs['path']
        self.prefs_separator=self.prefs['separator']
        self.prefs_notation=self.prefs['notation_format']

    def invoke_prefs(self):
        """This functions sets the radio buttons to current prefs values"""
        if self.prefs_separator == '':
            self.R1.invoke()
        elif self.prefs_separator == ',':
            self.R2.invoke()
        if self.prefs_notation == '.ly':
            self.R3.invoke()
        elif self.prefs_notation == '.mscz':
            self.R4.invoke()
        elif self.prefs_notation == '.sib':
            self.R5.invoke()
        elif self.prefs_notation == '.musx':
            self.R6.invoke()

    def choose_default(self):
        """This function calls system specific select path mecanism and displays new path value, not saved"""
        newPath = self.get_directory()
        self.path_label.set(newPath)
        self.prefs_path=newPath

    def reset_prefs(self):
        """This function dispays default values, not saved"""
        self.prefs_path=''
        self.set_temp_prefs('', '.ly')
        self.invoke_prefs()

    def set_temp_prefs(self, separator, notation):
        if separator != None:
            self.prefs_separator=separator
        if notation != None:
            self.prefs_notation=notation

    def save_temp_prefs(self):
        self.prefs={'path': self.prefs_path , 'separator':self.prefs_separator,
                    'notation_format':self.prefs_notation}
        self.controller.save_new_user_prefs(self.prefs)
        self.close_prefs()

    def display_saved_prefs(self):
        """ This function asks curent prefs to controller and display them"""
        self.get_saved_prefs()
        self.path_label.set(self.prefs_path)
        self.invoke_prefs()

    def close_prefs(self):
        """Manual single window Preferences Window destruction."""
        self.view.pref_win_statut = False
        self.preferences_window.destroy()

class AboutWindow():  
    def __init__(self, arg):
        self.val = arg
        self.filewin = Toplevel(self.val)
        text = Text(self.filewin)
        text.insert(INSERT,
"""\
Didacto o.1.4dev\n
Un projet développé pour vous par Marco de Freitas en confinement partiel.
""")
        text.config(wrap=WORD, state=DISABLED, padx=10, pady=10)
        text.pack()
 


class HelpWindow():
    def __init__(self, arg):
        self.root = arg
        self.filewin = Toplevel(self.root)
        text = Text(self.filewin)
        text.insert(INSERT,
"""\
Principe - Didacto est un logiciel d'aide à l'enseignement instrumental, qui facilite l'organisation didactique d'un répertoire d'exercices, d'études, ou authentique. \n
Didacto travail sur les partition au format pdf. Il faut donc au préalablre, lors de la création de vos pdf à partir d'un logiciel de notation ou à partir d'un logiciel de notation,
informer le champs mots-clés.
Fonctionnement - Choisir un répertoire à indexer. Didacto affiche une liste des mots-clés utilisés. Un clique sur un mot clé ouvre la liste des morceaux contenant ce mots clef\n
Un double-clique sur le nom du fichier ouvre le pdf. Un clique droit ouvre le fichier source de votre logiciel de notation.
""")
        text.insert(END,
"""\
En cliquant sur un mot-clés, Didacto affiche les titres des partitions. Double-cliquer sur le titre ouvre le pdf correspondant. Un clique droit ouvre le fichier Lylipond (.ly) correxpondant.
""")
        text.config(wrap=WORD, state=DISABLED)
        text.pack()

