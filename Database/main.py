#-*- coding: utf8 -*-
from database import Database
db = Database("db.sq3")
db.del_tables()
db.creat_tables()
tf1w = {}
tf1w['book1'] = 1.0
tf1w['book10'] = 10.0
tf1w['book11'] = 11.0
tf1w['book12'] = 12.0
print tf1w
tf2w = {}
tf2w['book2'] = 2.0
tf2w['book20'] = 20.0
tf2w['book21'] = 21.0
print tf2w
db.add_book_to_database('Book1','Auteur1',tf1w)
db.add_book_to_database('Book2','Auteur2',tf2w)
db.show_books()
db.show_words()
db.show_TFs()