#-*- coding: utf8 -*-
import sqlite3

class Database():
	
	def __init__(self, dataFile):
		# Chemin du fichier de la base de donnees
		self.dataFile = dataFile
		# Creation de la connexion et du curseur
		self.conn = sqlite3.connect(self.dataFile)
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
			self.cur.execute("""CREATE TABLE words(id_word INTEGER PRIMARY KEY AUTOINCREMENT, val VARCHAR(45))""")
			# Table des TFs
			self.cur.execute("""CREATE TABLE TF(id_book INTEGER NOT NULL, id_word INTEGER NOT NULL, val FLOAT, FOREIGN KEY (id_book) REFERENCES books(id_book), FOREIGN KEY (id_word) REFERENCES words(id_word), PRIMARY KEY (id_book, id_word))""")
		except:
			print('*** Requete SQL incorrecte creat_tables ***')

	# Ajout d'un livre
	def add_book(self, title_book, author_book):
		try:
			self.cur.execute("""INSERT INTO books(title, author) VALUES ('"""+title_book+"""', '"""+author_book+"""');""")
		except:
			print("*** Requete SQL incorrecte add_book("+title_book+") ***")
		else:
			print("add_book: "+title_book)
			print

	# Ajout d'un mot
	def add_word(self, val_word):
		try:
			self.cur.execute("""INSERT INTO words(val) VALUES ('"""+val_word+"""')""")
		except:
			print("*** Requete SQL incorrecte add_word("+val_word+") ***")
		else:
			print("add_word: "+val_word)
			print

	# Recherche id_book
	def id_book(self, title_book, author_book):
		try:
			self.cur.execute("""SELECT id_book FROM books WHERE title='"""+title_book+"""' AND author='"""+author_book+"""'""")
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
			print("*** Requete SQL incorrecte add_tf("+str(tf_word)+") ***")
		else:
			print("add_tf: "+str(tf_word))
			print

	# Ajout d'un livre dans la base de donnees
	def add_book_to_database(self, title_book, author_book, tf_words):
		# Recherche de l'id du livre
		idb = self.id_book(title_book, author_book)
		if idb == None:
			self.add_book(title_book, author_book)
			idb = self.id_book(title_book, author_book)
		for word in tf_words:
			# Recherche de l'id du mot
			idw = self.id_word(word)
			if idw == None:
				# Ajout du mot s'il n'y est pas encore
				self.add_word(word)
				idw = self.id_word(word)
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
				print('tf '+word+' dans '+title_book+': '+str(row[0]))
				return row[0]




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

	# Exécution d'une requête SQL
	def execute_sql(self, req):
		try:
			self.cur.execute(str(req))
		except:
			print("*** Requete SQL incorrecte execute_sql() ***")
		else:
			print(req)
			for r in self.cur:
				print (r)
			print

	# Sauvegarde de l'état actuel de la base de données
	def save_database(self):
		self.conn.commit()

	# Fermeture de la connexion
	def close_connection():
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
