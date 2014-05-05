# Specifications
''/!\ En cours de travail /!\'' 
Documents de Spécifications pour échanger avec les différents contributeurs

## Design Pattern Strategy
Je pense que serait bien qu'on utilise le design pattern ''Strategy'' pour chaque parties.
Petit rappel : ''Strategy'' est un patron de type comportemental grâce auquel des algorithmes peuvent être sélectionnés à la volée au cours du temps d'exécution selon certaines conditions (Merci Wikipédia).
Le but est donc de définir un objet pour chaque partie (parser, database, statistiques), qui comportera toutes les méthodes et objets nécessaires a son bon fonctionnement, et certains objets de type abstrait. Ces objets définiront de façon abstraite toutes les méthodes qu'on voudra faire passer dans ''Strategy''.

Voici un article (en anglais) qui décris une implémentation de ''Strategy'':
http://davidcorne.com/2013/01/21/strategy-pattern/
Voici le code source de l'exemple de cette article :
https://github.com/davidcorne/Design-Patterns-In-Python/blob/master/Behavioural/Strategy_old.py

### Architecture projet
![archi](Structure.png)

## Config
Pour utiliser de façon optimum le design pattern ''Strategy'', il faudrait créer un fichier de configuration qui décrirait quel stratégie utiliser à chaque étape du projet. Qui serait lu pour automatiquement à la création des obejts qui utilise des algorithmes ''Strategy''. Mais qui servirai aussi pour d'autre variable statique utile.

#### Exemple de fichier de configuration :  ".config"
```
database = "(mysql, postgresql, mongo, ...)"
similarité = "(cosine, euclidean, ...)"
...
bookDirectory = "/home/user/books"
...
```

## Parser
type de fichiers supportés
langue supportés
nombre de mots pris en compte

## Database
base de données supportés

Augmentation de la vitesse d'accès à la base :
Actuellement, les écritures dans la base sont séquentielles, ce qui ralentit l'ajout de livres à la base, l'ajout simultané de plusieurs livres n'étant pas possible. En rendant ces accès atomiques et asynchrones, en utilisant un SGBD (système de gestion de base de données), il serait alors possible de paralléliser les écritures et lectures, augmentant considérablement la vitesse d'ajout de livres à la base de données et le calcul des TF-IDF.

## Statistiques
similarités supportés

## Tools
### Minestones and Issues
//TODO
### Wiki
//TODO

----------------------
#Copyright and License
Copyright © 2014 Victor OUDIN <viktor.odex@gmail.com>

Copyright © 2014 Lala Tiana RANDRIAMPARANY <thinas4@gmail.com>

Copyright © 2014 Isabelle RICHARD <isabelle.richard89@gmail.com>

EbookMining is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EbookMining is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EbookMining.  If not, see <http://www.gnu.org/licenses/>.

![GPLv3](http://www.gnu.org/graphics/gplv3-88x31.png)

