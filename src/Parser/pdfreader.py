# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

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