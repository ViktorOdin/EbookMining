Copyright and License
----------------------
Copyright © 2014 Victor OUDIN <viktor.odex@gmail.com>
Copyright © 2014 Lala Tiana RANDRIAMPARANY <thinas4@gmail.com>
Copyright © 2014 Isabelle RICHARD <isabelle.richard89@gmail.com>

EbookMining is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EbookMining is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EbookMining.  If not, see <http://www.gnu.org/licenses/>.

![GPLv3](http://www.gnu.org/graphics/gplv3-88x31.png)

# Dépendances du projet

apt-get install jython python2.7
pip install sqlite3 nltk pypdf numpy

# Utilisation

## Ajout de livres à la base de données

python creation.py file.pdf  # ajout d'un document PDF
python creation.py directory # ajout de tous les documents PDF du répertoire 

# Temps d'exécution

Pour une base de données contenant 286 livres, le calcul des TF-IDF de tous les 
livres et de la matrice de similarités prend 3m53.576s.
Pour une base de données contenant 300 livres, le calcul des TF-IDF de tous les
livres et de la matrice de similarités prend 4m30.319s.
