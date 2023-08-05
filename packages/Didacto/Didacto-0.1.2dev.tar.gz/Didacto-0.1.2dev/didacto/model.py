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
#   contact:marco@sillage.ch

import os
import sys
import subprocess

from PyPDF2 import PdfFileReader
import PyPDF2


class CustomDict(dict):
    """Buit-in dict Class with à sort by key funtion added."""

    def sorted(self):
        """Sort the dictionnary by lowered key values, alphabetic order."""
        temp_dict = {}
        for item in sorted(self.keys(), key=str.lower):
            temp_dict[item] = sorted(self[item], key=lambda x: x['name'].
                                     lower())
        return temp_dict


class Model:
    def __init__(self, prefs):
        """Initialise prefs values retrieved by controller."""
        path = prefs['path']
        separator = prefs['separator']
        notation = prefs['notation_format']
        self.printo()  # test

    wordsDict = CustomDict()
    path = ''
    emptyDict = {}

    def printo(self):
        print(self.path)

# Sous-fonctions de scan_repertory()
    def get_info(self, path):
        """This function takes a pdf file path and returns the keywords"""
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f, strict=False)
            info = pdf.getDocumentInfo()
            key = info.get("/Keywords")
        return (key)

    def get_keywords_from_field(self, field):
        """This function takes the field 'keywords' of a pdf file and returns splitted values"""
        newKeywords = self.split_str(field)
        if newKeywords is None:
            newKeywords = "∅"
        return newKeywords

    def split_str(self, string, separator=None):
        """This function takes a string and a separator and return the splitted string"""
        if string is not None:
            try:
                output = string.split(separator)
            except:
                output = ''
            finally:
                return(output)

# Cette fonction parcours l'arborescence à partir du dossier sélectionné
# et récupère les mots clés
    def scan_repertory(self, path, recursive, words=None):
        """This function scan a directory for pdf file keywords."""
        if words is None:
            words = CustomDict()  # Evite le problème de {}mutable
        try:
            os.chdir(path)
        except:
            return
        else:
            for entry in os.scandir(path):
                if (not entry.name.startswith('.') and
                        entry.is_file() and
                        entry.name.endswith('.pdf')):
                    try:
                        pdfKey = self.get_info(entry.name)
                    except FileNotFoundError:
                        print("File does not exist:" + entry.name)

                    except:
                        print("Problem with file:" + entry.name)
                        continue  # si non pdf passe au fichier suivant
                    else:
                        keywords = (self.get_keywords_from_field(pdfKey))
                        if keywords is not None:
                            for i in keywords:
                                if not i in words:
                                    words[i] = [{"name": entry.name,
                                                 "path": entry.path}]
                                else:
                                    words[i].append({"name": entry.name,
                                                     "path": entry.path})
            for entry in os.scandir(path):
                if (not entry.name.startswith('.') and
                        entry.is_dir() and
                        recursive is True):
                    try:
                        os.chdir(entry.path)
                    except:
                        continue
                    else:
                        self.scan_repertory(entry.path, True, words)
        self.wordsDict = words
        self.wordsDict = self.wordsDict.sorted()
