# -*- coding: utf8 -*-

#!/usr/bin/env python2.7


##### IMPORTS #####

# Traitements sur le système
import os

# Interface graphique
from javax.swing import *
from java.awt import *
from javax.swing.table import DefaultTableModel

class MyExample:
	def __init__(self, dic_books, mat_sim):
		# Propriétés de la fenêtre
		frame = JFrame("EbookMining")
		frame.setSize(1000, 500) # FIXME
		frame.setLayout(BorderLayout())

		# Variables de classe
		self.dic_books = dic_books
		self.mat_sim = mat_sim
		self.tableData = []
		for id_book in dic_books:
			title, author = dic_books[id_book]
			self.tableData.append([id_book, title, author])
		colNames = ('id_book', 'Titre', 'Auteur')
		dataModel = DefaultTableModel(self.tableData, colNames)
		self.table = JTable(dataModel)
 
		scrollPane = JScrollPane()
		scrollPane.setPreferredSize(Dimension(800,400))
		scrollPane.getViewport().setView((self.table))

		panel = JPanel()
		panel.add(scrollPane)

		frame.add(panel, BorderLayout.CENTER)
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
		frame.setVisible(True)


if __name__ == '__main__':

	# Lecture de la liste des livres depuis un fichier CSV
	dic_books = {}
	books = open("books.csv")
	for line in books.readlines():
		line = line.replace("\n","")
		words = line.split("|")
		id_book = int(words[0])
		title = words[1]
		author = words[2]
		dic_books[id_book] = (title, author)
	books.close()

	# Calcul de la matrice depuis le fichier CSV
	mat_sim = {}
	csv = open("matrix.csv")
	for line in csv.readlines():
		line = line.replace("\n","")
		words = line.split("|")
		id_book_i = int(words[0])
		id_book_j = int(words[1])
		similarity = float(words[2])	
		if mat_sim.get(id_book_i) is None:
			mat_sim[id_book_i] = {}
		mat_sim[id_book_i][id_book_j] = similarity

	MyExample(dic_books, mat_sim)

	# # Boucle interactive : Renvoie la liste des livres les plus proches pour un identifiant donné
	# total_top = 20
	# quit = False
	# while not quit:
	# 	# Nettoyage de l'écran
	# 	os.system('clear')
	# 	id_book = input("Entrez l'identifiant du livre (entier): ")
	# 	# Tri des valeurs en fonction de la similarité
	# 	dic_sim = mat_sim[id_book]
	# 	sorted_dic_sim =  sorted(dic_sim.items(), key=lambda x: x[1], reverse=True)
	# 	current_top = 1
	# 	# Affichage des meilleurs similarités
	# 	title, author = dic_books[id_book]
	# 	print("Résultat pour " + title + ", de " + author)
	# 	for sim in sorted_dic_sim:
	# 		if current_top <= total_top:
	# 			cur_id_book = sim[0]
	# 			# title, author = db.get_book_by_id(cur_id_book)
	# 			title, author = dic_books[cur_id_book]
	# 			print(str(current_top) + ") Titre: " + title + " | Auteur: " + author)
	# 			current_top += 1
	# 		else:
	# 			break
	# 	x = input("\nVoulez-vous vous faire recommander d'autres livres ('o'/'n') ? ")
	# 	if x == 'n':
	# 		quit = True
