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

# Traitements sur le système
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
		#print("TFIDF du livre " + str(id_book) + " calculé")
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

def mat_similarities(tfidfs):
	"""Fabrique la matrice de similarite"""
	# Matrice de similarité
	mat_sim = {}
	# Récupération de la liste des identifiants des livres
	id_books = tfidfs.keys()
	# Création des dictionnaires de chaque livre
	for id_book in id_books:
		mat_sim[id_book] = {}
	# Calcul des similarités-cosinus
	for id_book_i in id_books:
		tfidf_book_i = np.array(tfidfs[id_book_i], dtype=np.float)
		for id_book_j in id_books[id_books.index(id_book_i)+1:]:
			tfidf_book_j = np.array(tfidfs[id_book_j], dtype=np.float)
			cos = st.similarity(tfidf_book_i, tfidf_book_j)
			mat_sim[id_book_i][id_book_j] = cos
			mat_sim[id_book_j][id_book_i] = cos
	return mat_sim

def is_valid(author, title):
	"""Vérifie si les métadonnées d'un PDF sont valides"""
	author_valid = author is not None and author != ""
	title_valid = title is not None and title != ""
	return author_valid and title_valid

def add_book_to_database(path):
	filepath = os.path.abspath(os.path.join(root, path))
	print("Ajout du fichier " + path)
	# Vérification de l'extension du fichier
	if filepath.endswith(".pdf"):
		# Lecture du fichier PDF
		pdf = parser.PdfReader(filepath)
		# Récupération des métadonnées du document
		author = pdf.getAuthor()
		title = pdf.getTitle()
		if is_valid(author, title) and not db.book_is_in_database(title, author):
			# Extraction du texte
			try:
				text = pdf.extractText()
			except:
				()
			else:
				# Récupération des TF de chacun des mots
				occurences = text.getOccurences()
				tfs = st.tf(text.getNumberOfWords(), occurences)
				# Ajout du livre à la base de données
				db.add_book_to_database(title, author, tfs)

				# Enregistrement des modifications
				db.save_database()

				# Affichage du nombre actuel de livres dans la base
				print("Nombre de livres dans la base de données: " + str(db.number_books()))



if __name__ == '__main__':

	# Connexion à la base de donnée
	databasePath = "db.sq3"
	db = db.Database(databasePath)

	# Vérification de l'existence des tables
	db.creat_tables()

	if len(sys.argv) < 2:
		usage()

	else:
		directoryPath = sys.argv[1]
		# Récupération de la liste des fichiers à parser
		for root, dirs, files in os.walk(directoryPath):
			for path in files:
				add_book_to_database(path)

	# Calcul des similarités avec un livre
	tfidfs = tfidfs()

	# Calcul de la matrice de similarités
	mat_sim = mat_similarities(tfidfs)

	# Boucle interactive : Renvoie la liste des livres les plus proches pour un identifiant donné
	total_top = 20
	quit = False
	while not quit:
		# Nettoyage de l'écran
		os.system('clear')
		# Affichage de la liste des livres
		db.show_books()
		id_book = input("Entrez l'identifiant du livre (entier): ")
		# Tri des valeurs en fonction de la similarité
		dic_sim = mat_sim[id_book]
		sorted_dic_sim =  sorted(dic_sim.items(), key=lambda x: x[1], reverse=True)
		current_top = 1

		# Affichage des meilleurs similarités
		title, author = db.get_book_by_id(id_book)
		print(u"Résultat pour " + title + u", de " + author)
		for sim in sorted_dic_sim:
			if current_top <= total_top:
				cur_id_book = sim[0]
				title, author = db.get_book_by_id(cur_id_book)
				print(str(current_top) + ") Titre: " + title + " | Auteur: " + author)
				current_top += 1
			else:
				break
		x = input("\nVoulez-vous vous faire recommander d'autres livres ('o'/'n') ? ")
		if x == 'n':
			quit = True
					
	# Fermeture de la connexion
	db.close_connection()
