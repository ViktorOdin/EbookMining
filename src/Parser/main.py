# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"Ce programme est une démonstration du module pdfreader.py"

import sys
from pdfreader import PdfReader

import sys
sys.path.append("../Database")
from database import Database

if __name__ == '__main__':

	databasePath = "db.sq3"

	# Connexion à la base de données
	db = Database(databasePath)

	# Vérification de l'existence des tables
	db.creat_tables()

	if len(sys.argv) < 2:
		print("Usage: python main.py filepath\n"
			+ "\toù filepath est le chemin du fichier PDF à lire")

		# Affichage du top 10
		db.top10_book()

	else:
		filepath = sys.argv[1]
		pdf = PdfReader(filepath)

		databasePath = "db.sq3"

		# Connexion à la base de données
		db = Database(databasePath)

		# Vérification de l'existence des tables
		db.creat_tables()

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
		text = pdf.extractText()
		print(text.getNumberOfWords())

		# Ecriture des occurences de chaque mot du document dans foo.txt
		foo = open('/tmp/foo.txt', 'w')
		occurences = text.getOccurences()
		for word in occurences:
			foo.write(word.encode('utf8', 'ignore') + ": " 
				+ str(occurences[word]) + "\n")
		foo.close()