# -*- coding: utf8 -*-

#!/usr/bin/env python2.7


##### IMPORTS #####

# Traitements sur le système
import os

# Interface graphique
from javax.swing import *
from java.awt import *
from java.awt.event import *
from javax.swing.table import DefaultTableModel

# Variables globales
global mat_sim, dic_books

class ResultFrame:
	def __init__(self, result):
		# Propriétés de la fenêtre
		frame = JFrame("Resultats de la recommandation")
		frame.setSize(1000, 500)
		frame.setLayout(BorderLayout())

		# Variables de classe
		self.dic_books = dic_books
		self.mat_sim = mat_sim
		colNames = ('id_book', 'Titre', 'Auteur')
		self.dataModel = DefaultTableModel(result, colNames)
		self.table = JTable(self.dataModel)
 
		scrollPane = JScrollPane()
		scrollPane.setPreferredSize(Dimension(800,400))
		scrollPane.getViewport().setView((self.table))

		panel = JPanel()
		panel.add(scrollPane)

		frame.add(panel, BorderLayout.CENTER)
		frame.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE)
		frame.setVisible(True)

class MainFrame:
	def __init__(self, dic_books, mat_sim):
		# Propriétés de la fenêtre
		frame = JFrame("EbookMining")
		frame.setSize(1000, 500)
		frame.setLayout(BorderLayout())

		# Variables de classe
		self.dic_books = dic_books
		self.mat_sim = mat_sim
		# Tri des livres en fonction du titre
		sorted_dic_books =  sorted(dic_books.items(), key=lambda x: x[1])
		self.tableData = []
		for book in sorted_dic_books:
			id_book = book[0]
			title, author = book[1]
			self.tableData.append([id_book, title, author])
		colNames = ('id_book', 'Titre', 'Auteur')
		self.dataModel = DefaultTableModel(self.tableData, colNames)
		self.table = JTable(self.dataModel)
		# self.table.setAutoResizeMode(JTable.AUTO_RESIZE_ALL_COLUMNS)
 
		scrollPane = JScrollPane()
		scrollPane.setPreferredSize(Dimension(800,400))
		scrollPane.getViewport().setView((self.table))

		panel = JPanel()
		panel.add(scrollPane)

		button = JButton("►", actionPerformed=self.recommand)
		panel.add(button)

		frame.add(panel, BorderLayout.CENTER)
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
		frame.setVisible(True)

	def getSelectedBook(self):
		"""Retourne l'identifiant du livre sélectionné"""
		index = self.table.getSelectedRow()
		return self.dataModel.getValueAt(index, 0)

	def recommand(self, event):
		"""Trie les livres par ordre de similarité et les envoie dans une table"""
		id_book = self.getSelectedBook()
		# Tri des valeurs en fonction de la similarité
		dic_sim = mat_sim[id_book]
		sorted_dic_sim =  sorted(dic_sim.items(), key=lambda x: x[1], reverse=True)
		result = []
		title, author = dic_books[id_book]
		for sim in sorted_dic_sim:
			cur_id_book = sim[0]
			title, author = dic_books[cur_id_book]
			result.append([cur_id_book, title, author])
		ResultFrame(result)

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

	MainFrame(dic_books, mat_sim)

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
