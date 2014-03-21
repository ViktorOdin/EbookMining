# Dépendances du projet

pip install sqlite3 nltk pypdf numpy
apt-get install jython

# Utilisation

## Ajout de livres à la base de données

python creation.py file.pdf  # ajout d'un document PDF
python creation.py directory # ajout de tous les documents PDF du répertoire 

# Temps d'exécution

Pour une base de données contenant 286 livres, le calcul des TF-IDF de tous les 
livres et de la matrice de similarités prend 3m53.576s.
Pour une base de données contenant 300 livres, le calcul des TF-IDF de tous les
livres et de la matrice de similarités prend 4m30.319s.
