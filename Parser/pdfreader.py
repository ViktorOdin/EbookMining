# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"""
TODO
"""

import pyPdf

class PdfReader():

	def __init__(self, filepath):
		"TODO"
		self.filepath = filepath
		self.pdf = pyPdf.PdfFileReader(open(filepath, "rb"))
		self.metadata = self.extractMetadata()
		self.text = self.extractText()
		
	def getAuthor(self):
		"Returns the author of the document, or None if it is not defined"
		return self.metadata.get('/Author')

	def getTitle(self):
		"Returns the title of the document, or None if it is not defined"
		return self.metadata.get('/Title')

	def getText(self):
		"Returns the text of the document."
		return self.text

	def extractMetadata(self):
		"Extracts the metadata of the document."
		return self.pdf.getDocumentInfo()

	def extractText(self):
		"Extracts the text of the document."
		text = ""
		for page in self.pdf.pages:
			text += page.extractText()
		return text
