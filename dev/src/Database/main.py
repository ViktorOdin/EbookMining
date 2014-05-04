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