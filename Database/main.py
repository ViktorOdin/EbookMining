#-*- coding: utf8 -*-
from database import Database
db = Database("db.sq3")
db.del_tables()
db.creat_tables()
tf1w = {}
tf1w['mot1'] = 1.0
# tf1w['mot10'] = 10.0
# tf1w['mot11'] = 11.0
# tf1w['mot12'] = 12.0
print tf1w
tf2w = {}
tf2w['mot1'] = 3.0
tf2w['mot2'] = 2.0
# tf2w['mot20'] = 20.0
# tf2w['mot21'] = 21.0
print tf2w
db.add_book_to_database('Book1','Auteur1',tf1w)
db.add_book_to_database('Book2','Auteur2',tf2w)
db.show_books()
db.show_words()
db.show_TFs()
db.execute_sql("""SELECT * FROM TF, words WHERE TF.id_word = words.id_word""")
db.tf_word('mot1', 'Book1','Auteur1')
db.tf_word('mot1', 'Book2','Auteur2')