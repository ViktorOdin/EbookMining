# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"Ce programme est une démonstration du module pdfreader.py"

import sys
from pdfreader import PdfReader

if __name__ == '__main__':
	"Méthode main"
	if len(sys.argv) < 2:
		print("Usage: python main.py filepath\n"
			+ "\toù filepath est le chemin du fichier PDF à lire")
	else:
		filepath = sys.argv[1]
		pdf = PdfReader(filepath)

		# Récupération des métadonnées du document
		author = pdf.getAuthor()
		title = pdf.getTitle()

		# Affichage des métadonnées du document
		if author is not None:
			print("Auteur du document: " + pdf.getAuthor())
		else:
			print("L'auteur du document n'est pas indiqué")
		if title is not None:
			print("Titre du document: " + pdf.getTitle())
		else:
			print("Le titre du document n'est pas indiqué")

		# Affichage du nombre de mots du document
		print(pdf.text.getNumberOfWords())

		# Ecriture des occurences de chaque mot du document dans foo.txt
		foo = open('foo.txt', 'w')
		occurences = pdf.text.countOccurences()
		for word in occurences:
			foo.write(word.encode('utf8', 'ignore') + ": " 
				+ str(occurences[word]) + "\n")
		foo.close()