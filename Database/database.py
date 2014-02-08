import sqlite3

class Database():
	
	def __init__(self, dataFile):
		super(Database, self).__init__()
		# Chemin du fichier de la base de donnees
		self.dataFile = dataFile
		# Creation de la connexion et du curseur
		self.conn = sqlite3.connect(self.dataFile)
		self.cur = self.conn.cursor()

	# Suppression des tables
	def del_tables(self):
		try:
			self.cur.execute("DROP TABLE authors")
			self.cur.execute("DROP TABLE books")
		except:
			print('*** Requete SQL incorrecte del_tables ***')

	# Creation des tables
	def creat_tables(self):
		try:
			# Table des auteurs
			self.cur.execute("CREATE TABLE authors(id_author INTEGER NOT NULL, lastname TEXT, firstname TEXT, PRIMARY KEY (id_author))")
			# Table des livres
			self.cur.execute("CREATE TABLE books(id_book INTEGER NOT NULL, title TEXT, category TEXT, id_author INTEGER, PRIMARY KEY (id_book), FOREIGN KEY (id_author) REFERENCES authors(id_author))")
		except:
			print('*** Requete SQL incorrecte creat_tables ***')

	# Ajout d'un auteur
	def add_author(self, id_author, lastname_author, firstname_author):
		try:
			self.cur.execute("INSERT INTO authors(id_author, lastname, firstname) VALUES ("+id_author+", '"+lastname_author+"', '"+firstname_author+"')")
			self.cur.execute("SELECT * FROM authors")
		except:
			print("*** Requete SQL incorrecte add_author("+lastname_author+") ***")
		else:
			print("add_author: "+lastname_author+" "+firstname_author)
			print()

	# Recherche id_author
	def id_author(self, lastname_author, firstname_author):
		try:
			self.cur.execute("SELECT id_author FROM authors WHERE lastname='"+lastname_author+"' AND firstname='"+firstname_author+"'")
		except:
			print("*** Requete SQL incorrecte id_author("+lastname_author+", "+firstname_author+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				return row[0]

	# Ajout d'un livre
	def add_book(self, id_book, title_book, category_book, id_author):
		try:
			self.cur.execute("INSERT INTO books(id_book, title, category, id_author) VALUES ("+id_book+", '"+title_book+"', '"+category_book+"', "+id_author+")")
			#self.cur.execute("SELECT * FROM books")
		except:
			print("*** Requete SQL incorrecte add_book("+title_book+") ***")
		else:
			print("add_book: "+title_book)
			print()

	def add_book_to_database(self, title_book, lastname_author, firstname_author, category_book):
		ida = self.id_author(lastname_author, firstname_author)
		if ida == None:
			try:
				self.cur.execute("SELECT count(*) FROM authors")
			except :
				print("*** Requete SQL incorrecte add_book_to_database("+title_book+") ***")
			else:
				row = self.cur.fetchone()
				if row:
					ida = row[0]
					self.add_author(str(ida),lastname_author,firstname_author)
		try:
			self.cur.execute("SELECT count(*) FROM books")
		except :
			print("*** Requete SQL incorrecte add_book_to_database("+title_book+") ***")
		else:
			row = self.cur.fetchone()
			if row:
				idb = row[0]
				self.add_book(str(idb), title_book, category_book, str(ida))

	# Afficher les livres
	def show_books(self):
		try:
			self.cur.execute("SELECT * FROM books")
		except :
			print("*** Requete SQL incorrecte show_books() ***")
		else:
			print ("books:")
			for b in self.cur:
				print(b)
			print()

	# Afficher les auteurs
	def show_authors(self):
		try:
			self.cur.execute("SELECT * FROM authors")
		except :
			print("*** Requete SQL incorrecte show_authors() ***")
		else:
			print ("authors:")
			for a in self.cur:
				print(a)
			print()

	# Exécuter une requête SQL
	def execute_sql(self, req):
		try:
			self.cur.execute(str(req))
		except :
			print("*** Requete SQL incorrecte execute_sql() ***")
		else:
			print(req)
			return self.cur.fetchall()

	# Confirmation des changements
	def confirm(self):
		choice = input("Enregistrer l'état actuel de la base de données (o/n) ? ")
		if choice[0] == "o" or choice[0] == "O":
			self.conn.commit()
			print("Enregistrement OK!")
		else:
			print("Enregistrement annulé!")
		self.conn.close()
