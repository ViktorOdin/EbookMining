# -*- coding: utf8 -*-
#!/usr/bin/env python2.7
#
# EbookMining/dev/src/Database/__init__.py
#
# Copyright © 2014 Victor OUDIN <viktor.odex@gmail.com>
# Copyright © 2014 Lala Tiana RANDRIAMPARANY <thinas4@gmail.com>
# Copyright © 2014 Isabelle RICHARD <isabelle.richard89@gmail.com>
#
# This file is part of EbookMining.
#
#  EbookMining is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  EbookMining is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with EbookMining.  If not, see <http://www.gnu.org/licenses/>.

"Ce module enregistre le contenu et les métadonnées d'un fichier PDF."

import pyPdf
from text import Text, clean

global exception_no_space
exception_no_space = "no_space_in_document"

class PdfReader():

	def __init__(self, filepath):
		"""Enregistre le contenu et les métadonnées d'un fichier PDF.
		[filepath] est le chemin vers le fichier PDF."""
		self.filepath = filepath
		self.pdf = pyPdf.PdfFileReader(open(filepath, "rb"))
		self.author = self.pdf.getDocumentInfo().get('/Author')
		self.title = self.pdf.getDocumentInfo().get('/Title')

	### Accesseurs 
		
	def getAuthor(self):
		"Retourne l'auteur du document, ou None s'il n'est pas défini."
		if self.author is None:
			return None
		else:
			return clean(self.author)

	def getTitle(self):
		"Retourne le titre du document, ou None s'il n'est pas défini."
		if self.title is None:
			return None
		else:
			return clean(self.title)

	### Méthodes internes

	def extractText(self):
		"Extrait le texte du document."
		text = ""
		for page in self.pdf.pages:
			tmp = page.extractText()
			if tmp.count(' ') == 0:
				raise Exception(exception_no_space)
			text += tmp
		return Text(text)