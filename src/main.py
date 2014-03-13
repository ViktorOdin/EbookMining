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

	databasePath = "db.sq3"

	# Connexion à la base de données
	db = db.Database(databasePath)

	# Vérification de l'existence des tables
	db.creat_tables()

	if len(sys.argv) < 2:
		print("Usage: python main.py directory\n"
			+ "\toù directory est le chemin répertoire contenant"
			+ "les livres à ajouter à la base")

	else:
		directoryPath = sys.argv[1]

		# Récupération de la liste des fichiers à parser
		for root, dirs, files in os.walk(directoryPath):
			for file in files:
				filepath = os.path.abspath(os.path.join(root, file))

				# Lecture du fichier PDF
				pdf = parser.PdfReader(filepath)

				# Récupération des métadonnées du document
				author = pdf.getAuthor()
				title = pdf.getTitle()

				if not db.book_is_in_database(title, author):
					# Extraction du texte
					text = pdf.extractText()

					# TODO delete me
					print("Livre en cours de traitement: " + title)

					# Récupération des TF de chacun des mots
					occurences = text.getOccurences()
					tfs = st.tf(text.getNumberOfWords(), occurences)

					# Ajout du livre à la base de données
					db.add_book_to_database(title, author, tfs)

					# Enregistrement des modifications
					db.save_database()

				else:
					print("Livre deja dans la base: " + title)

	# Affichage de la liste des livres
	db.show_books()

	# Affichage du nombre de mots
	print("Nombre de mots dans la base: " + str(db.number_words()))

	# Affichage du top 20 d'un livre
	# for i in range (db.number_books()):
	# 	print("Top 20 du " + str(i) + "è livre:")
	# 	db.top20_book(i)

	#calcul IDF
	nb_books = db.number_books()
	print(nb_books)
	dic = db.dic_word_nbbooks()
	print(1)
	dic_idf = st.dic_idf(nb_books, dic)
	print(2)
	dic_tf = db.dic_tf_book(1)
	print(3)
	print(dic_tf["dqsdqs"])
	dic_tfidf = {}
	for word in dic_idf:
		dic_tfidf[word] = (dic_tf[word]*dic_idf[word])
	print(dic_idf)


	# Fermeture de la connexion
	db.close_connection()
