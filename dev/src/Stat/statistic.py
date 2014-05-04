# -*- coding: utf8 -*-
# !/usr/bin/env python2.7
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

import numpy as np


def tf(n_words, dic_occu):
    dic_tf = {}
    for word in dic_occu.keys():
        dic_tf[word] = (dic_occu[word] / float(n_words))
    return dic_tf


def idf(n_books, n_books_with_word):
    return np.log(n_books / float(n_books_with_word))


def dic_idf(n_books, dic_occu_books_with_word):
    dic_idf = {}
    for word in dic_occu_books_with_word.keys():
        dic_idf[word] = idf(n_books, dic_occu_books_with_word[word])
    return dic_idf


def similarity(list_tfidf1, list_tfidf2):
    # Produit scalaire
    dot_product = np.dot(list_tfidf1, list_tfidf2)
    # Normes euclidiennes
    euclidean_norm1 = np.sqrt(np.dot(list_tfidf1, list_tfidf1))
    euclidean_norm2 = np.sqrt(np.dot(list_tfidf2, list_tfidf2))

    if (euclidean_norm1 * euclidean_norm2) == 0:
        return 0.0
    else:
        return dot_product / (euclidean_norm1 * euclidean_norm2)
