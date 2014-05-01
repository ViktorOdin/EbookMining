#!/usr/bin/env python2.7

import numpy as np
import math

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

def similarity(list_tfidf1, list_tfidf2):
	# Produit scalaire
	dot_product = np.dot(list_tfidf1, list_tfidf2)
	# Normes euclidiennes
	euclidean_norm1 = np.sqrt(np.dot(list_tfidf1,list_tfidf1))
	euclidean_norm2 = np.sqrt(np.dot(list_tfidf2,list_tfidf2))

	if (euclidean_norm1 * euclidean_norm2) == 0:
		return 0.0
	else:
		return dot_product / (euclidean_norm1 * euclidean_norm2)
	