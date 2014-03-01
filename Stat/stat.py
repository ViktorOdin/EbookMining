#!/usr/bin/env python2.7

import numpy as np

def tf (nbr_mot, dico_occu):
  dico_tf = {}
  for mot in dico_occu.keys():
    dico_tf[mot]=(dico_occu[mot]/ float(nbr_mot))
  return dico_tf
  
def idf (nbr_livre, nbr_livre_ayant_mot):
  return np.log(nbr_livre/ float(nbr_livre_ayant_mot))
