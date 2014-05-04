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

# Traitements sur le système
import os

# Interface graphique
from javax.swing import *
from java.awt import *
from java.awt.event import *
from javax.swing.table import DefaultTableModel

# Variables globales
global mat_sim, dic_books, window_height, window_width
window_height = 1200
window_width = 800

class MainFrame:
	def __init__(self, dic_books, mat_sim):
		# Propriétés de la fenêtre
		frame = JFrame("EbookMining")
		frame.setSize(window_height, window_width)
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

		# Suppression de la colonne des identifiants dans l'affichage
		column = self.table.getColumnModel().getColumn(0)
		self.table.removeColumn(column)

		scrollPane = JScrollPane()
		scrollPane.setPreferredSize(Dimension(window_height - 100, window_width - 100))
		scrollPane.getViewport().setView((self.table))

		panel = JPanel()
		panel.add(scrollPane)

		button = JButton("Chercher", actionPerformed=self.recommand)
		panel.add(button)

		frame.add(panel, BorderLayout.CENTER)
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
		frame.setVisible(True)

	def getSelectedBooks(self):
		"""Retourne la liste des identifiants des livres sélectionnés"""
		# index = self.table.getSelectedRow()
		# return self.dataModel.getValueAt(index, 0)
		indexes = self.table.getSelectedRows()
		result = []
		for index in indexes:
			result.append(self.dataModel.getValueAt(index, 0))
		return result

	def recommand(self, event):
		"""Trie les livres par ordre de similarité et les envoie dans une table"""
		id_books = self.getSelectedBooks()
		dic_sim = mat_sim[id_books[0]]
		# Suppression des entrées correspondant aux identifiants recherchés
		for id_book in id_books:
			try:
				del dic_sim[id_book]
			except:
				()
		# Somme des similarités pour chaque livre
		for id_book in id_books[1:]:
			cur_dic_sim = mat_sim[id_book]
			for key in dic_sim:
				dic_sim[key] += cur_dic_sim[key]
		# Tri des valeurs en fonction de la similarité
		sorted_dic_sim =  sorted(dic_sim.items(), key=lambda x: x[1], reverse=True)
		result = []
		for sim in sorted_dic_sim:
			cur_id_book = sim[0]
			title, author = dic_books[cur_id_book]
			result.append([cur_id_book, title, author])
		if len(id_books) > 1:
			ResultFrame(result)
		else:
			title, author = dic_books[id_book]
			ResultFrame(result, title, author)

class ResultFrame:
	def __init__(self, result, title="", author=""):
		# Propriétés de la fenêtre
		if title == "" and author == "":
			frame = JFrame("Resultats pour la recommandation des livres selectionnes")
		else:
			frame = JFrame("Resultats de la recommandation pour '" + title + "', de " + author)
		frame.setSize(window_height, window_width)
		frame.setLayout(BorderLayout())

		# Variables de classe
		self.dic_books = dic_books
		self.mat_sim = mat_sim
		colNames = ('id_book', 'Titre', 'Auteur')
		self.dataModel = DefaultTableModel(result, colNames)
		self.table = JTable(self.dataModel)

		# Suppression de la colonne des identifiants dans l'affichage
		column = self.table.getColumnModel().getColumn(0)
		self.table.removeColumn(column)

		scrollPane = JScrollPane()
		scrollPane.setPreferredSize(Dimension(window_height - 100, window_width - 100))
		scrollPane.getViewport().setView((self.table))

		panel = JPanel()
		panel.add(scrollPane)

		frame.add(panel, BorderLayout.CENTER)
		frame.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE)
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

	# Lecture de la matrice de similarités depuis le fichier CSV
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

	# Lancement de l'interface graphique
	MainFrame(dic_books, mat_sim)
