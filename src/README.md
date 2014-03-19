Conception :

À chaque fois qu'un livre est ajouté, vérifier qu'aucune exception n'a été
levée, et si c'est le cas, enregistrer les changements dans la base.
Sinon : ?

Quand on ajoute un livre, récupérer uniquement son titre et son auteur (ne pas
parser le texte tout de suite), vérifier que le livre ne se trouve pas déjà
dans la base de données, et l'ajouter si ce n'est pas le cas.

Pour une base de données contenant 286 livres, 
le calcul des TFIDF de tous les livres et de la matrice de similarités prend 3m53.576s.