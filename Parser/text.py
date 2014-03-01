# -*- coding: utf8 -*-

#!/usr/bin/env python2.7

"""
Ce module permet de travailler sur un texte : le nettoyer, calculer le 
nombre d'occurence de chacun de ses mots.
"""

import string
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords

class Text():

	def __init__(self, originalText):
		"Nettoie le texte passé en paramètre"
		self.text = self.clean(originalText)

	def clean(self, text):
		"Retire les chiffres et la ponctuation d'un texte."
		# Encodage de unicode vers utf8
		tmp = text.encode('utf8')
		tmp = tmp.translate(None, string.digits)
		# Réencodage de utf8 vers unicode
		text = unicode(tmp, 'utf8')
		return text

	def countOccurences (self):
		"""Compte les occurences de chaque mot du texte	et retourne un 
		dictionnaire dont les clés sont les mots et les valeurs	le nombre 
		d'occurences."""
		occ = {}
		# Découpage du texte en liste
		words_tmp = WordPunctTokenizer().tokenize(self.text)
		# Suppression des mots les plus courants dans la langue française
		stemmer = FrenchStemmer()
		stop = stopwords.words('french')
		words = [w for w in words_tmp if w.encode('utf8') not in stop]
		# Calcul des occurences
		for word in words:
			# Retirer le genre et le nombre du mot
			word = stemmer.stem(word)
			# Ignorer la ponctuation
			if word not in string.punctuation:
				if word in occ:
					occ[word] += 1
				else:
					occ[word] = 1
		return occ

	def getNumberOfWords(self):
		"Retourne le nombre de mots du texte."
		return len(self.text)

