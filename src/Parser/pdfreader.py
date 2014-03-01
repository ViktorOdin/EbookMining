
# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"Ce module enregistre le contenu et les métadonnées d'un fichier PDF."

import pyPdf
from text import Text

class PdfReader():

	def __init__(self, filepath):
		"""Enregistre le contenu et les métadonnées d'un fichier PDF.
		[filepath] est le chemin vers le fichier PDF."""
		self.filepath = filepath
		self.pdf = pyPdf.PdfFileReader(open(filepath, "rb"))
		self.metadata = self.extractMetadata()
		self.text = self.extractText()

	### Accesseurs 
		
	def getAuthor(self):
		"Retourne l'auteur du document, ou None s'il n'est pas défini."
		return self.metadata.get('/Author')

	def getTitle(self):
		"Retourne le titre du document, ou None s'il n'est pas défini."
		return self.metadata.get('/Title')

	def getText(self):
		"Retourne le texte du document."
		return self.text

	### Méthodes internes

	def extractMetadata(self):
		"Extrait les métadonnées du document."
		return self.pdf.getDocumentInfo()

	def extractText(self):
		"Extrait le texte du document."
		text = ""
		for page in self.pdf.pages:
			text += page.extractText()
		return Text(text)