# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

# Utilisation des modules du projet
import sys
sys.path.append("./Database")
import Database as db
sys.path.append("./Parser")
import Parser as parser
sys.path.append("./Stat")
import Stat as st

# Lecture des fichiers d'un répertoire
import os

if __name__ == '__main__':
	"Méthode main"
	if len(sys.argv) < 2:
		print("Usage: python main.py directory\n"
			+ "\toù directory est le chemin répertoire contenant"
			+ "les livres à ajouter à la base")
	else:
		directoryPath = sys.argv[1]
		databasePath = "db.sq3"

		# Connexion à la base de données
		db = db.Database(databasePath)

		# Vérification de l'existence des tables
		# TODO
		# db.creat_tables()

		# Récupération de la liste des fichiers à parser
		for root, dirs, files in os.walk(directoryPath):
			for file in files:
				filepath = os.path.abspath(os.path.join(root, file))

				# Lecture du fichier PDF
				pdf = parser.PdfReader(filepath)

				# Récupération des métadonnées du document
				author = pdf.getAuthor()
				title = pdf.getTitle()

				# Récupération des TF de chacun des mots
				occurences = pdf.text.getOccurences()
				tfs = st.tf(pdf.text.getNumberOfWords(), occurences)

				# Ajout du livre à la base de données
				db.add_book_to_database(title, author, tfs)

		# Affichage de la liste des livres
		db.show_books()