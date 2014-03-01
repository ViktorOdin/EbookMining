#!/usr/bin/env python2.7

import numpy as np

def tf (n_words, dic_occu):
  dic_tf = {}
  for word in dic_occu.keys():
    dic_tf[word]=(dic_occu[word]/ float(n_words))
  return dic_tf
  
def idf (n_books, n_books_with_word):
  return np.log(n_books / float(n_books_with_word))

def dic_idf (n_books, dic_occu_books_with_word):
  dic_idf = {}
  for word in dic_occu_books_with_word.keys():
    dic_idf[word]=idf(n_books,dic_occu_books_with_word[word])
  return dic_idf