# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"""
This program is a demonstration of the module pdfreader.py
"""

import sys
from pdfreader import PdfReader

if __name__ == '__main__':
	"Main method"
	if len(sys.argv) < 2:
		print("Usage: python main.py filepath\n"
			+ "\toù filepath est le chemin du fichier PDF à lire")
	else:
		filepath = sys.argv[1]
		pdf = PdfReader(filepath)

		# Get the metadata of the document
		author = pdf.getAuthor()
		title = pdf.getTitle()

		# Print the metadata of the document
		if author is not None:
			print("Auteur du document: " + pdf.getAuthor())
		else:
			print("L'auteur du document n'est pas indiqué")
		if title is not None:
			print("Titre du document: " + pdf.getTitle())
		else:
			print("Le titre du document n'est pas indiqué")

		# Print the 1000 first characters of the document
		print(pdf.getText()[:1000])