# -*- coding: utf8 -*-

#!/usr/bin/env python2.7


##### IMPORTS #####

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

# Calcul de la similarité-cosinus
import numpy as np


##### VARIABLES GLOBALES #####

global databasePath
global db

##### FONCTIONS #####
	
def usage():
	"""Affiche l'aide d'utilisation."""
	print("Usage: python main.py directory\n"
		+ "\toù directory est le chemin répertoire contenant"
		+ "les livres à ajouter à la base")

def tfidfs():
	"""Calcule le TF-IDF de tous les livres de la base"""
	# Récupération de la liste des id_book de la base
	id_books = db.get_id_books()
	# Nombre de livres dans la base
	nb_books = len(id_books)
	# Récupération, pour chaque mot, du nombre de livres où chaque mot apparaît
	occ_in_books = db.dic_idword_nbbooks()
	# Construction d'un dictionnaire des IDF de la base de données
	dic_idf = st.dic_idf(nb_books, occ_in_books)
	# Construction d'un dictionnaire associant son TF-IDF à chaque id_book
	tfidfs = {}
	for id_book in id_books:
		dic_tf = db.dic_tf_book(id_book)
		tfidf = []
		for idword in dic_idf:
			tfidf.append(float(dic_tf.get(idword,0)) * float(dic_idf[idword]))
		tfidfs[id_book] = tfidf
		print("TFIDF du livre " + str(id_book) + " calculé")
	return tfidfs

def similarities(tfidfs, id_book):
	"""Calcule les livres les plus proches de id_book"""
	# Dictionnaire des similarités
	dic_sim = {}
	# TFIDF du livre à comparer
	tfidf_book = np.array(tfidfs[id_book], dtype=np.float)
	# Calcul des similarités-cosinus de id_book avec les autres livres
	for tfidf in tfidfs:
		if tfidfs != id_book:
			tfidf_tmp = np.array(tfidfs[tfidf], dtype=np.float)
			cos = st.similarity(tfidf_book, tfidf_tmp)
			dic_sim[tfidf] = cos
	return dic_sim

if __name__ == '__main__':

	databasePath = "db.sq3"

	# Connexion à la base de donnéedatabase = "db.sq3"
	db = db.Database(databasePath)

	# Vérification de l'existence des tables	
	db.creat_tables()

	if len(sys.argv) < 2:
		usage()

	else:
		directoryPath = sys.argv[1]

		# Récupération de la liste des fichiers à parser
		for root, dirs, files in os.walk(directoryPath):
			for file in files:
				filepath = os.path.abspath(os.path.join(root, file))
				print("Traitement du livre: " + filepath)

				# Vérification de l'extension du fichier
				if not filepath.endswith(".pdf"):
					print("Format du fichier invalide")

				else:
					# Lecture du fichier PDF
					pdf = parser.PdfReader(filepath)

					# Récupération des métadonnées du document
					author = pdf.getAuthor()
					title = pdf.getTitle()

					if author is None or author == "" or title is None or title == "":
						print("Métadonnées invalides: " + filepath)

					elif not db.book_is_in_database(title, author):
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

<<<<<<< HEAD
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
	dic = db.dic_idword_nbbooks()
	dic_idf = st.dic_idf(nb_books, dic)
	dic_tf1 = db.dic_tf_book(28)
	dic_tf2 = db.dic_tf_book(33)
	
	list_tfidf1 = []
	list_tfidf2 = []
	for idword in dic_idf:
		list_tfidf1.append(float(dic_tf1.get(idword,0))*float(dic_idf[idword]))
		list_tfidf2.append(float(dic_tf2.get(idword,0))*float(dic_idf[idword]))
	
	cos1 = st.similarity(np.array(list_tfidf1, dtype=np.float),np.array(list_tfidf2, dtype=np.float))
	print(cos1)
	cos1 = st.similarity(np.array(list_tfidf1, dtype=np.float),np.array(list_tfidf1, dtype=np.float))
	print(cos1)

=======
	# # Affichage de la liste des livres
	# db.show_books()

	# # Affichage du top 20 d'un livre
	# # for i in range (db.number_books()):
	# # 	print("Top 20 du " + str(i) + "è livre:")
	# # 	db.top20_book(i)

	# Calcul des similarités avec un livre
	tfidfs = tfidfs()

	while True:
		id_book = input("Entrez l'identifiant du livre (entier): ")
		dic_sim = similarities(tfidfs, id_book)
		# Tri des valeurs en fonction de la similarité
		sorted_dic_sim =  sorted(dic_sim.items(), key=lambda x: x[1], reverse=True)
		tmp = 0
		for sim in sorted_dic_sim:
			if tmp < 20:
				print(sim)
				tmp += 1
			else:
				break
>>>>>>> 0492e039141805d2face40942dd03920483b20e8

	# Fermeture de la connexion
	db.close_connection()
