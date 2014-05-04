# -*- coding: utf8 -*-
#!/usr/bin/env python2.7
#
# EbookMining/dev/src/Database/database.py
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

import sqlite3

# Temps d'attente de la libération du verrou, en secondes
TIME = 120 

class Database():
	
	def __init__(self, dataFile):
		# Chemin du fichier de la base de donnees
		self.dataFile = dataFile
		# Creation de la connexion et du curseur
		self.conn = sqlite3.connect(self.dataFile, TIME)
		self.cur = self.conn.cursor()

	# Suppression des tables
	def del_tables(self):
		try:
			self.cur.execute("DROP TABLE words")
			self.cur.execute("DROP TABLE books")
			self.cur.execute("DROP TABLE TF")
		except:
			print('*** Requete SQL incorrecte del_tables ***')

	# Création des tables
	def creat_tables(self):
		try:
			# Table des livres
			self.cur.execute("""CREATE TABLE books(id_book INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(45), author VARCHAR(45))""")
			# Table des mots
			self.cur.execute("""CREATE TABLE words(id_word INTEGER PRIMARY KEY AUTOINCREMENT, val VARCHAR(45), nb_books INTEGER)""")
			# Table des TFs
			self.cur.execute("""CREATE TABLE TF(id_book INTEGER NOT NULL, id_word INTEGER NOT NULL, val FLOAT, FOREIGN KEY (id_book) REFERENCES books(id_book), FOREIGN KEY (id_word) REFERENCES words(id_word), PRIMARY KEY (id_book, id_word))""")
		except:
			print('*** Requete SQL incorrecte creat_tables ***')

	# Ajout d'un livre
	def add_book(self, title_book, author_book):
		try:
			self.cur.execute('''INSERT INTO books(title, author) VALUES ("'''+title_book+'''", "'''+author_book+'''");''')
		except:
			print("*** Requete SQL incorrecte add_book("+title_book+") ***")
		else:
			# print("add_book: "+title_book)
			# print
			()

	# Ajout d'un mot
	def add_word(self, val_word):
		try:
			self.cur.execute("""INSERT INTO words(val, nb_books) VALUES ('"""+val_word+"""', 1)""")
		except:
			print("*** Requete SQL incorrecte add_word("+val_word+") ***")
		else:
			# print("add_word: "+val_word)
			# print
			()

	# Récupération de la liste des id_book
	def get_id_books(self):
		try:
			self.cur.execute("""SELECT id_book FROM books""")
		except:
			print("*** Requete SQL incorrecte get_id_books() ***")
		else:
			id_books = []
			for b in self.cur:
				id_books.append(b[0])
			return id_books

	# Recherche id_book
	def id_book(self, title_book, author_book):
		try:
			self.cur.execute('''SELECT id_book FROM books WHERE title="'''+title_book+'''" AND author="'''+author_book+'''"''')
		except:
			print("*** Requete SQL incorrecte id_book("+title_book+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				return row[0]

	# Recherche id_word
	def id_word(self, word):
		try:
			self.cur.execute("""SELECT id_word FROM words WHERE val='"""+word+"""'""")
		except:
			print("*** Requete SQL incorrecte id_word("+word+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				return row[0]

	# Ajout du TF d'un mot dans TF
	def add_tf(self, id_book, id_word, tf_word):
		try:
			self.cur.execute("""INSERT INTO TF(id_book, id_word, val) VALUES ("""+str(id_book)+""", """+str(id_word)+""", """+str(tf_word)+""")""")
		except:
			# print("*** Requete SQL incorrecte add_tf("+str(tf_word)+") ***")
			()
		else:
			# print("add_tf: "+str(tf_word))
			# print
			()

	# Vérification de l'existence du livre dans la base de donnees
	def book_is_in_database(self, title_book, author_book):
		# Recherche de l'id du livre
		idb = self.id_book(title_book, author_book)
		if idb == None:
                        return False
                else:
                        return True
                
	# Ajout d'un livre dans la base de donnees
	def add_book_to_database(self, title_book, author_book, tf_words):
		# Recherche de l'id du livre
		idb = self.id_book(title_book, author_book)
		if idb == None	:
			self.add_book(title_book, author_book)
			idb = self.id_book(title_book, author_book)
		for word in tf_words:
			# Recherche de l'id du mot
			idw = self.id_word(word)
			if idw == None:
				# Ajout du mot s'il n'y est pas encore
				self.add_word(word)
				idw = self.id_word(word)
			else:
				# Incrémentation du nombre de livres où le mot apparaît
				self.cur.execute("""UPDATE words SET nb_books = nb_books + 1 WHERE id_word = """ + str(idw))
			self.add_tf(str(idb), str(idw), tf_words[word])

	# Recherche du TF d'un mot dans un livre
	def tf_word(self, word, title_book, author_book):
		# Recherche des id du livre et du mot
		idw = str(self.id_word(word))
		idb = str(self.id_book(title_book, author_book))
		try:
			self.cur.execute("""SELECT val FROM TF WHERE id_book="""+idb+""" AND id_word="""+idw)
		except:
			print("*** Requete SQL incorrecte tf_word("+word+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				# print('tf '+word+' dans '+title_book+': '+str(row[0]))
				return row[0]

	# Nombre de mots dans la base
	def number_words(self):
		try:
			self.cur.execute('''SELECT count(*) FROM words''')
		except:
			print("*** Requete SQL incorrecte number_words() ***")
		else:
			row = self.cur.fetchone()
			return row[0]

	# Nombre de mots dans la base
	def number_books(self):
		try:
			self.cur.execute('''SELECT count(*) FROM books''')
		except:
			print("*** Requete SQL incorrecte number_books() ***")
		else:
			row = self.cur.fetchone()
			return row[0]	

	def get_word_by_id(self, id_word):
		"""Renvoie la valeur d'un mot en fonction de son id"""
		try:
			self.cur.execute('''SELECT val FROM words WHERE id_word = ''' + str(id_word))
		except:
			print("*** Requete SQL incorrecte get_word_by_id() ***")
		else:
			row = self.cur.fetchone()
			return row[0]

			self.cur.execute("""CREATE TABLE books(id_book INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(45), author VARCHAR(45))""")

	def get_book_by_id(self, id_book):
		"""Renvoie le couple (titre, auteur) d'un livre en fonction de son id"""
		try:
			self.cur.execute("""SELECT title, author FROM books WHERE id_book =""" + str(id_book))
		except:
			print("*** Requete SQL incorrecte get_book_by_id() ***")
		else:
			row = self.cur.fetchone()
			return row[0], row[1]

	def top20_book(self, id_book):
		cur = self.conn.cursor()
		try:
			cur.execute('''SELECT id_word, val FROM TF WHERE id_book = ''' + str(id_book) + ''' ORDER BY val DESC LIMIT 20''')
		except:
			print("*** Requete SQL incorrecte top10_book() ***")
		else:
			for b in cur:
				word = self.get_word_by_id(str(b[0]))
				print(word + ": " + str(b[1]))
			print

	# Affichage des livres
	def show_books(self):
		try:
			self.cur.execute("""SELECT * FROM books""")
		except:
			print("*** Requete SQL incorrecte show_books() ***")
		else:
			print ("books:")
			for b in self.cur:
				print(b)
			print

	# Affichage des mots
	def show_words(self):
		try:
			self.cur.execute("""SELECT * FROM words""")
		except:
			print("*** Requete SQL incorrecte show_words() ***")
		else:
			print ("words:")
			for a in self.cur:
				print(a)
			print

	# Affichage des TFs
	def show_TFs(self):
		try:
			self.cur.execute("""SELECT * FROM TF""")
		except:
			print("*** Requete SQL incorrecte show_TFs() ***")
		else:
			print ("TFs:")
			for a in self.cur:
				print(a)
			print

	# IDF
	def dic_idword_nbbooks(self):
		"""Récupère, pour chaque mot, le nombre de livres où il apparaît."""
		try:
			self.cur.execute("""SELECT id_word, nb_books FROM words""")
		except:
			print("*** Requete SQL incorrecte idf() ***")
		else:
			dic_nbbooks = {}
			for a in self.cur:
				id_word = str(a[0])
				nbbooks = str(a[1])
				dic_nbbooks[id_word] = nbbooks
			return dic_nbbooks

	def dic_tf_book(self, id_book):
		try:
			self.cur.execute("""SELECT id_word, val FROM TF WHERE id_book ="""+ str(id_book))
		except:
			print("*** Requete SQL incorrecte idf() ***")
		else:
			dic_tf = {}
			for a in self.cur:
				id_word = str(a[0])
				tf = str(a[1])
				dic_tf[id_word] = tf
			return dic_tf

	# Exécution d'une requête SQL
	def execute_sql(self, req):
		try:
			self.cur.execute(str(req))
		except:
			print("*** Requete SQL incorrecte execute_sql() ***")
		else:
			# print(req)
			# for r in self.cur:
			# 	print (r)
			# print
			()

	# Sauvegarde de l'état actuel de la base de données
	def save_database(self):
		self.conn.commit()

	# Fermeture de la connexion
	def close_connection(self):
		self.conn.close()

	# Demande de confirmation des changements
	# et fermeture de la connexion
	def confirm(self):
		choice = input("""Enregistrer l'état actuel de la base de données ("o"/"n") ? """)
		if choice[0] == "o" or choice[0] == "O":
			self.save_database()
			print("Enregistrement OK!")
		else:
			print("Enregistrement annulé!")
		self.conn.close()
