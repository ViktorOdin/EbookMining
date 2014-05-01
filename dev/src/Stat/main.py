#!/usr/bin/env python2.7

import statistic as st

dic1={'mot':3, 'cigalle':3, 'onomatopee':1, 'toto':3, 'kangourou':2, 'general':1, 'mortier':1, 'le':5, 'et':4, 'pistache':1} #24
dic2={'mot':1, 'cafard':4, 'gros':1, 'titi':4, 'marsupial':1, 'colonnel':2, 'fourchette':1, 'la':5, 'et':4, 'pistache':3} #26
dic3={'verbe':2, 'cafard':1, 'gros':2, 'titi':2, 'lapin':3, 'colonnel':4, 'fourchette':3, 'la':1, 'et':2, 'pistache':1} #21

tf1=st.tf(24,dic1)
tf2=st.tf(26,dic2)
tf3=st.tf(21,dic3)

dicTmp={'mot':2, 'cigalle':1, 'onomatopee':1, 'toto':1, 'kangourou':1, 'general':1, 'mortier':1, 'le':1, 'et':3, 'pistache':3, 'cafard':2, 'gros':2, 'titi':2, 'marsupial':1, 'colonnel':2, 'fourchette':2, 'la':2, 'verbe':1, 'lapin':1}

all_idf=st.dic_idf(3,dicTmp)

print(tf1)
print(tf2)
print(tf3)
print(all_idf)