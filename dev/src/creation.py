# -*- coding: utf8 -*-
#!/usr/bin/env python2.7
#
# EbookMining/dev/src/Database/__init__.py
#
# Copyright © 2014 Victor OUDIN <viktor.odex@gmail.com>
# Copyright © 2014 Lala Tiana RANDRIAMPARANY <thinas4@gmail.com>
# Copyright © 2014 Isabelle RICHARD <isabelle.richard89@gmail.com>
#
# This file is part of EbookMining.
#
#  EbookMining is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  EbookMining is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with EbookMining.  If not, see <http://www.gnu.org/licenses/>.

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

	# Création des tables
	# db.creat_tables()

	if len(sys.argv) > 1:
		path = sys.argv[1]
		if os.path.isdir(path):
			directoryPath = path
			# Récupération de la liste des fichiers à parser
			for root, dirs, files in os.walk(directoryPath):
				for path in files:
					add_book_to_database(path)
		else:
			add_book_to_database(path)

	# Calcul des similarités avec un livre
	print("Calcul des TF-IDFS...")
	tfidfs = tfidfs()

	# Calcul de la matrice de similarités
	print("Calcul de la matrice de similarité...")
	mat_sim = mat_similarities(tfidfs)

	# Ecriture de la liste des livres dans un fichier CSV
	print("Ecriture de la liste des livres dans 'books.csv'")
	books = open("books.csv", 'w')
	for id_book in db.get_id_books():
		title, author = db.get_book_by_id(id_book)
		books.write(str(id_book) + "|" + title.encode('utf8') + "|" + author.encode('utf8') + "\n")
	books.close()

	# Ecriture de la matrice dans un fichier CSV
	print("Ecriture de la matrice de similarités dans 'matrix.csv'")
	csv = open("matrix.csv", 'w')
	for id_book_i in mat_sim:
		for id_book_j in mat_sim[id_book_i]:
			csv.write(str(id_book_i) + "|" + str(id_book_j) +  "|" + str(mat_sim[id_book_i][id_book_j]) + "\n")
	csv.close()
					
	# Fermeture de la connexion
	db.close_connection()
