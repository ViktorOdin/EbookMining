#-*- coding: utf8 -*-
import sqlite3 as sq3

class Database():
	
	def __init__(self, dataFile):
		# Create database file's path
		self.dataFile = dataFile
		# Create cursor and connection
		self.conn = sq3.connect(self.dataFile)
		self.cur = self.conn.cursor()

	# Delete tables
	def del_tables(self):
		try:
			self.cur.execute("DROP TABLE words")
			self.cur.execute("DROP TABLE books")
			self.cur.execute("DROP TABLE TF")
		except:
			print('*** Requete SQL incorrecte del_tables ***')

	# Create tables
	def creat_tables(self):
		try:
			# Book table
			self.cur.execute("""CREATE TABLE books(id_book INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(45), author VARCHAR(45), nb_words INTEGER)""")
			# Word table
			self.cur.execute("""CREATE TABLE words(id_word INTEGER PRIMARY KEY AUTOINCREMENT, val VARCHAR(45))""")
			# TF table
			self.cur.execute("""CREATE TABLE TF(id_book INTEGER NOT NULL, id_word INTEGER NOT NULL, val FLOAT, FOREIGN KEY (id_book) REFERENCES books(id_book), FOREIGN KEY (id_word) REFERENCES words(id_word), PRIMARY KEY (id_book, id_word))""")
		except:
			print('*** Requete SQL incorrecte creat_tables ***')

	# Add a book
	def add_book(self, title_book, author_book, nb_words):
		try:
			self.cur.execute("""INSERT INTO books(title, author, nb_words) VALUES ('"""+title_book+"""', '"""+author_book+"""', """+str(nb_words)+""");""")
		except:
			print("*** Requete SQL incorrecte add_book("+title_book+") ***")
		else:
			print("add_book: "+title_book)
			print

	# Add a word
	def add_word(self, val_word):
		try:
			self.cur.execute("""INSERT INTO words(val) VALUES ('"""+val_word+"""')""")
		except:
			print("*** Requete SQL incorrecte add_word("+val_word+") ***")
		else:
			print("add_word: "+val_word)
			print

	# Find id_book
	def id_book(self, title_book, author_book):
		try:
			self.cur.execute("""SELECT id_book FROM books WHERE title='"""+title_book+"""' AND author='"""+author_book+"""'""")
		except:
			print("*** Requete SQL incorrecte id_book("+title_book+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				return row[0]

	# Find id_word
	def id_word(self, word):
		try:
			self.cur.execute("""SELECT id_word FROM words WHERE val='"""+word+"""'""")
		except:
			print("*** Requete SQL incorrecte id_word("+word+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				return row[0]

	# Add TF in TF table
	def add_tf(self, id_book, id_word, tf_word):
		try:
			self.cur.execute("""INSERT INTO TF(id_book, id_word, val) VALUES ("""+str(id_book)+""", """+str(id_word)+""", """+str(tf_word)+""")""")
		except:
			print("*** Requete SQL incorrecte add_tf("+str(tf_word)+") ***")
		else:
			print("add_tf: "+str(tf_word))
			print

	# Add a book in the database
	def add_book_to_database(self, title_book, author_book, tf_words, nb_words):
		# Find the book's id
		idb = self.id_book(title_book, author_book)
		if idb == None:
			self.add_book(title_book, author_book, nb_words)
			idb = self.id_book(title_book, author_book)
		for word in tf_words:
			# Find the word's id
			idw = self.id_word(word)
			if idw == None:
				# Add the word in database if it isn't already in it 
				self.add_word(word)
				idw = self.id_word(word)
			self.add_tf(str(idb), str(idw), tf_words[word])

	# Find the TF value of a word in a book
	def tf_word(self, word, title_book, author_book):
		# Find word's id and book's id
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




	# Show all books
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

	# Show all words
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

	# Show all TFs
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

	# Execute a SQL request
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

	# Save the actual state of database
	def save_database(self):
		self.conn.commit()

	# Close the connection
	def close_connection(self):
		self.conn.close()

	# Save database and close connection
	def confirm(self):
		choice = input("""Enregistrer l'état actuel de la base de données ("o"/"n") ? """)
		if choice[0] == "o" or choice[0] == "O":
			self.save_database()
			print("Enregistrement OK!")
		else:
			print("Enregistrement annulé!")
		self.conn.close()
