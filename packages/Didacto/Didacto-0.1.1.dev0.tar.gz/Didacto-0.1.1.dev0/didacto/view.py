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

from os import *

from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import ttk
from tkinter import *

class Tree():
    def __init__(self,root):
        pass

class View():
    def __init__(self, root, model,controller):

        self.model = model
        self.root = root
        self.controller = controller


        self.pref_win_statut = False #contrôle l'état des fenêtre uniques (aide, à propos, préférences)

        self.menubar = Menu(root)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Choisir Dossier', accelerator='ctrl+p', command=self.choose_folder)
        self.filemenu.add_command(label='Rafraîchir', accelerator='ctrl+r',  command=self.tree_refresh)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Préférences', command=self.call_preferences_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quiter', accelerator='ctrl+q', command=self.controller.quit) # underline='0'
        self.menubar.add_cascade(label='Fichier', menu=self.filemenu)
        
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='Aide', command=self.create_help_window)
        self.helpmenu.add_command(label='A propos', command=self.create_about_window)
        self.menubar.add_cascade(label='Aide', menu=self.helpmenu)

        self.root.bind('<Control-p>', self.select_folder)
        self.root.bind('<Control-r>', self.refresh_treeview)
        self.root.bind('<Control-q>', self.close_programm)
        self.root.config(menu=self.menubar)


        self.frame0 = Frame(root)
        self.frame0.text =StringVar('')
        l1 = Label(self.frame0, textvariable=self.frame0.text)
        l1.pack()
        
        self.frame0.pack()

        self.checkbox_value = BooleanVar()
        checkbox = Checkbutton(root, text="Inclure sous-dossiers", variable=self.checkbox_value, command=self.do_nothing)
        checkbox.pack()

        
        
        self.frame1 = Frame(root)
        
        self.buttonChoose = Button(root, text='Choisir dossier', command=self.choose_folder)
        self.buttonRefresh = Button(root, text='Rafraîchir', command=self.tree_refresh)

        
        self.tv = ttk.Treeview(root, columns=['files','path'], 
                  selectmode='browse')
        self.tv.column('#0', minwidth=100, stretch=True)
        self.tv.column('files', minwidth=250, stretch=True)
        self.tv.column('path', minwidth=250, stretch=True)
        self.tv.heading('#0', text='Mots-clef')
        self.tv.heading('files', text='Fichiers', anchor='center')
        self.tv.heading('path', text='Chemin', anchor='center')
        self.tv.pack(expand=True, fill='both')
        self.yscroll = Scrollbar(root, orient='vertical', command=self.tv.yview)
        self.yscroll.pack(side='right', fill='y')

        self.collapsebox_value = BooleanVar()
        collapsebox = Checkbutton(root, text="Ouvrir/Fermer tout", variable=self.collapsebox_value, command=lambda : self.collapse_nodes(self.collapsebox_value.get()))
        collapsebox.pack(side = TOP)

        for widget in [self.buttonChoose,self.buttonRefresh,self.tv,self.yscroll]:  #
            widget.pack(side=LEFT)


            
        self.frame1.pack()
        
        self.tv.bind('<<TreeviewSelect>>', self.prout)
        self.tv.bind('<<TreeviewOpen>>', self.prouti)
        self.tv.bind('<<TreeviewClose>>', self.prouta)
        self.tv.bind("<Double-1>", self.OnDoubleClick)
        self.tv.bind("<ButtonRelease-3>", self.OnRightClick)
        

    def collapse_nodes(self, value):
                        for tree_index in range(len(self.model.wordsDict)):
                            self.tv.item(tree_index, open = value)
        
        

# gestion des racourcis clavier

    def select_folder(self,event):
        self.choose_folder()

    def refresh_treeview(self,event):
        self.tree_refresh()

    def close_programm(self,event):
        self.controller.quit()


 # création des fenêtres singleton       
        
    def create_about_window(self):
        a=AboutWindow(self.root)

    def create_help_window(self):
        a=HelpWindow(self.root)


    def call_preferences_window(self):
        if self.pref_win_statut == False:
            self.create_preferences_window()


    def create_preferences_window(self):
        
        self.preferences_check = True
        self.preferences_window=Toplevel()
        self.preferences_window.wm_title("Préférences")
        self.preferences_window.protocol('WM_DELETE_WINDOW', self.close_pref)

        self.buttonChooseDefaultPath = Button(self.preferences_window, text='Choisir un dossier a indexer par défaut', command=self.choose_default)
        self.buttonChooseDefaultPath.pack()

        self.default_path =StringVar('')
        self.l1 = Label(self.preferences_window, textvariable=self.default_path)
        self.l1.pack()
        

        self.l2 =Label(self.preferences_window, text="Séparateur par défaut")
        self.l2.pack()

        self.separator = StringVar()
        R1 = Radiobutton(self.preferences_window, text="espace", variable=self.separator, value=" ",
                  command=self.do_nothing)
        R1.pack( anchor=CENTER )
        R2 = Radiobutton(self.preferences_window, text="virgule", variable=self.separator, value=",",
                  command=self.do_nothing)
        R2.pack( anchor = CENTER )
        


        self.l3 =Label(self.preferences_window, text="Format des fichiers de notation")
        self.l3.pack()

        self.notation_format = StringVar()
        R3 = Radiobutton(self.preferences_window, text="Lylipond", variable=self.notation_format, value=".ly ",
                  command=self.do_nothing)
        R3.pack( anchor=CENTER )
        R4 = Radiobutton(self.preferences_window, text="Musescore", variable=self.notation_format, value=".mscz",
                  command=self.do_nothing)
        R4.pack( anchor = CENTER )
        
        R5 = Radiobutton(self.preferences_window, text="Sibélius", variable=self.notation_format, value=".sib",
                  command=self.do_nothing)
        R5.pack( anchor = CENTER )
        R6 = Radiobutton(self.preferences_window, text="Final", variable=self.notation_format, value=".musx",
                  command=self.do_nothing)
        R6.pack( anchor = CENTER )
        

        self.l4 =Label(self.preferences_window, text="Position des fichiers de notation")
        self.l4.pack()

        self.notation_position = BooleanVar()
        R7 = Radiobutton(self.preferences_window, text="Identique au fichier PDF", variable=self.notation_position, value=True,
                  command=self.do_nothing)
        R7.pack( anchor=CENTER )
        R8 = Radiobutton(self.preferences_window, text="Tous dans le même dossier", variable=self.notation_position, value=False,
                  command=self.choose_default_notation)
        R8.pack( anchor = CENTER )
        

        self.default_notation_path =StringVar('')
        self.l1 = Label(self.preferences_window, textvariable=self.default_notation_path)
        self.l1.pack()

        self.buttonResetPreferences = Button(self.preferences_window, text='Reset', command=self.do_nothing)
        self.buttonResetPreferences.pack(side = RIGHT)

        self.buttonDiscardPreferences = Button(self.preferences_window, text='Annuler', command=self.do_nothing)
        self.buttonDiscardPreferences.pack(side = RIGHT)

        self.buttonSavePreferences = Button(self.preferences_window, text='Sauvegarder', command=self.do_nothing)
        self.buttonSavePreferences.pack(side = RIGHT)

        R1.invoke()
        R3.invoke()
        R7.invoke()





        
        

        
      #  for widget in [self.text,self.l1,self.buttonChooseDefaultPath]:  #
       #     widget.pack(side=BOTTOM)
  
        

    def choose_default(self):
        newPath = self.get_directory()
        self.default_path.set(newPath)

    def choose_default_notation(self):
        newPath = self.get_directory()
        self.default_notation_path.set(newPath)
       
      
       
       


    def close_pref(self):
        self.pref_win_statut = False
        self.preferences_window.destroy()
        




    def do_nothing(self):
        pass


# Test sur la sélection par la souris


    def prout(self, event):
        print("selected:" +self.tv.focus())

    def prouti(self, caca):
        print("Open")

    def prouta(self, caca):
        print("Close")

# Gestion de la souris

    def OnDoubleClick(self,event):
        item = self.tv.identify("item", event.x, event.y)
        self.controller.run_file(self.tv.item(item)["values"][1])

    def OnRightClick(self,event):
        item = self.tv.identify("item", event.x, event.y)
        path = self.tv.item(item)["values"][1][:-4]+'.ly'
        self.controller.run_file(path)

    



# Cette fonction efface le contenu de l'arbre
            
    def tree_delete(self,size):
        if size > 0:
            for idid in range(size):
                self.tv.delete(idid)

# Cette fonction recrée un arbre à partir du dictionnaire

    def tree_repopulate(self):
        tree_index=0
        for key in self.model.wordsDict:
            self.tv.insert('', index= tree_index, iid=tree_index , text=key , values=[''])
            for list_index in range(len(self.model.wordsDict[key])):
                self.tv.insert(tree_index, index = tree_index , text = '', values=[self.model.wordsDict[key][list_index]['name'],self.model.wordsDict[key][list_index]['path']])
            tree_index+=1

    def tree_refresh(self): #oh copie de code de choose_folder
        treeSize=len(self.model.wordsDict)
        path=self.frame0.text.get()
        recursive=self.checkbox_value.get()
        self.model.scan_repertory(path,recursive)
        self.tree_delete(treeSize)
        self.tree_repopulate()


    def get_directory(self):
            givenPath =  filedialog.askdirectory()
            if givenPath is not None:
                return givenPath



# Cette fontion déclanché par le bouton choisir gère la sélection du dossier de départ
# déclanche l'algorythme de récupération des mots clés, puis gère l'affichage du nouvel arbre

    def choose_folder(self):
        treeSize=len(self.model.wordsDict)
        newPath = self.get_directory()
        self.frame0.text.set(newPath)
        recursive = self.checkbox_value.get()
        self.model.scan_repertory(newPath,recursive)
        self.tree_delete(treeSize)
        self.tree_repopulate()


class Menubar():
    def __init(self,arg):
        self.root=arg
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Choisir Dossier', accelerator='ctrl+p', command=self.choose_folder)
        self.filemenu.add_command(label='Rafraîchir', accelerator='ctrl+r',  command=self.tree_refresh)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quiter', accelerator='ctrl+q', command=self.controller.quit) # underline='0'
        self.menubar.add_cascade(label='Fichier', menu=self.filemenu)
        
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='Aide', command=self.create_help_window)
        self.helpmenu.add_command(label='A propos', command=self.create_about_window)
        self.menubar.add_cascade(label='Aide', menu=self.helpmenu)

        self.root.bind('<Control-p>', self.select_folder)
        self.root.bind('<Control-r>', self.refresh_treeview)
        self.root.bind('<Control-q>', self.close_programm)
        self.root.config(menu=self.menubar)
    
class AboutWindow(): # motif singleton copié de https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    class __OnlyOne: 
        def __init__(self,arg):
            self.val = arg
            self.filewin = Toplevel(self.val)
            text = Text(self.filewin)
            
            text.insert( INSERT,
"""\
Didacto \n
Un projet développé pour vous par Marco de Freitas en confinement partiel.
""")
            
            text.config(wrap=WORD, state=DISABLED,padx=10, pady=10)
            text.pack()      
    instance = None    
    def __init__(self, arg):
        if not AboutWindow.instance:
            AboutWindow.instance = AboutWindow.__OnlyOne(arg)
        else:
            AboutWindow.instance.val = arg
            


    


class HelpWindow():
    class __OnlyOne: 
        def __init__(self,arg):
            self.val = arg
            self.filewin = Toplevel(self.val)
            text = Text(self.filewin)
        
            text.insert(INSERT,
 """\
Principe - Didacto est un logiciel d'aide à l'enseignement instrumental, qui facilite l'organisation didactique d'un répertoire authentique. \n
Pour l'utiliser il convient d'abord d'assigner à chaque oeuvre de votre répertoire enseigné un certrain nombre de mots-clés par exemple: débutant, technique, etc. \n
Fonctionnement - Choisir un répertoire à indexer. Didacto affiche une liste des mots-clés utilisés. Un clique sur un mot clé ouvre la liste des morceaux contenant ce mots clef\n
""")
            text.insert(END,
"""\
En cliquant sur un mot-clés, Didacto affiche les titres des partitions. Double-cliquer sur le titre ouvre le pdf correspondant. Un clique droit ouvre le fichier Lylipond (.ly) correxpondant.
""")
            text.config(wrap=WORD, state=DISABLED)
            text.pack()

    instance = None
    def __init__(self,arg):
        if not HelpWindow.instance:
            HelpWindow.instance = HelpWindow.__OnlyOne(arg)
        else:
            HelpWindow.instance.val = arg
        

        

    
class SingletonWindow():
    class __OnlyOne:
        def __init__(self, arg, content):
            content(arg)
    instance = None
    def __init__(self, arg, content):
        if not SingletonWindow.instance:
            SingletonWindow.instance = SingletonWindow.__OnlyOne(arg,content)
        else:
            HelpWindow.instance.val = arg
    
