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

"""
Ce module permet de travailler sur un texte : le nettoyer, calculer le
nombre d'occurence de chacun de ses mots.
"""

import re
import string
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords


def clean(text):
    """Retourne la liste des mots nettoyés de leurs chiffres
    et de leurs accents, et passés en minuscules."""
    # Encodage de unicode vers utf8
    tmp = text.encode('utf8')
    # Suppression des chiffres
    tmp = tmp.translate(None, string.digits)
    # Suppression des accents
    tmp = remove_accents(tmp)
    # Réencodage de utf8 vers unicode
    text = unicode(tmp, 'utf8')
    text = string.lower(text)
    return text


def remove_accents(ch, encod='utf-8'):
    """Supprime les accents sans changer la casse (majuscules et minuscules)"""
    conv = False
    if not isinstance(ch, unicode):
        ch = unicode(ch, encod, 'replace')
        conv = True
    alpha1 = u"àÀâÂäÄåÅçÇéÉèÈêÊëËîÎïÏôÔöÖùÙûÛüÜÿŸ"
    alpha2 = u"aAaAaAaAcCeEeEeEeEiIiIoOoOuUuUuUyY"
    x = ""
    for c in ch:
        k = alpha1.find(c)
        if k >= 0:
            x += alpha2[k]
        else:
            x += c
    if conv:
        x = x.encode(encod)
    return x


class Text():

    def __init__(self, originalText):
        "Nettoie le texte passé en paramètre"
        self.words = self.split_words(clean(originalText))
        self.occurences = self.countOccurences()

    # Accesseurs

    def getNumberOfWords(self):
        "Retourne le nombre de mots du texte."
        return len(self.words)

    def getOccurences(self):
        """Retourne le dictionnaire des occurences de chaque mot
        dans le document."""
        return self.occurences

    # Méthodes internes

    def split_words(self, text):
        """Retourne la liste des mots d'un texte."""
        # Suppression de la ponctuation
        text = re.sub("[\W]", " ", text, 0, 0)
        return text.split()

    def countOccurences(self):
        """Compte les occurences de chaque mot du texte et retourne un
        dictionnaire dont les clés sont les mots et les valeurs le nombre
        d'occurences."""
        occ = {}
        stemmer = FrenchStemmer()
        # Découpage du texte en liste
        words_tmp = self.words
        # Suppression des mots les plus courants dans la langue française
        stop = stopwords.words('french')
        words = [w for w in words_tmp if string.lower(w).encode('utf8') not in stop]
        # Calcul des occurences
        for word in words:
            # Retirer le genre et le nombre du mot
            word = stemmer.stem(word)
            if word in occ:
                occ[word] += 1
            else:
                occ[word] = 1
        return occ
