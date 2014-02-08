from database import Database
db = Database("db.sq3")
db.del_tables()
db.creat_tables()
db.add_book_to_database('Book1','Pren1','Nom1','Cat1')
db.add_book_to_database('Book2','Pren2','Nom2','Cat2')
db.add_book_to_database('Book3','Pren1','Nom1','Cat1')
db.show_books()
db.show_authors()
rep = db.execute_sql("select * from books natural join authors where books.id_author='0'")
for r in rep:
	print(r)
db.confirm()