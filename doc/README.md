**/!\ En cours de travail /!\**  
Documents de Spécifications pour échanger avec les différents contributeurs.
# Specifications Théoriques de fouilles de textes
***

## Théories du Prétraitement.
### Etiquetage des mots.
Deux types de catégories:
- catégories “ouvertes”: classes qui ont un très grand nombre de membres, et aux quelles sont souvent ajoutés de nouveaux membres (noms, verbes, adjectifs, adverbes).
- catégories “fermées” ou fonctionnelles: classes qui ont seulement quelques membres et une fonction grammaticale claire (déterminants, prépositions, pronoms, conjonctions de coordination et de subordination).

### Racinisation.
- Lovins.
- Porter.

### Indexation.
un index indique, pour chaque mot dans la collection:
- la liste des documents qui le contiennent
- pour chaque document, sa fréquence d'occurrence

l'index peut également contenir des informations de position:
- pour chaque document, ses positions dans le document

## Requêtes
### Prétraitements sur la requête
les prétraitements effectués sur la requête doivent être les mêmes que ceux effectués lors de la phase d'indexation.  
prétraitements possibles:
- tokenisation
- mise en minuscule
- désaccentuation des lettres accentuées
- racinisation
- repérage de mots composés

### Synonymes
extension possible de la requête par l'ajout des synonymes des termes de la requête (utilisation d'un dictionnairede synonymes).

## Théories des Modèles.
### Modèles booléens.
une représentation mathématique du contenu d'un document, selon une approche ensembliste. Un document est caractérisé par la présence ou l'absence de chaque terme dans son contenu. les requêtes sont alors traitées comme des expressions logiques, et un document du corpus est considéré comme pertinent uniquement quand son contenu est vrai pour l'expression de la requête. Utilisation possible de la distance de Jaccard.  
selon la requête, classer les documents en deux classes:
- pertinents
- non pertinents  

classification de documents:
- étant donné un ensemble de classes prédéfinies
- on assigne à chaque document une ou plusieurs de ces classes

### Modèles vectorielles.
une représentation mathématique du contenu d'un document, selon une approche algébrique.
- représentation des documents et requêtes:
  - un document = vecteur dans un espace de grande dimension
  - chaque dimension correspondà un mot de la collection
  - chaque composante est le poids du mot associé dans le document ou la requête
- proximité spatiate et proximité sémantique:
  - les documents les plus pertinents sont représentés par les vecteurs les plus proches de celui de la requête
  - les documents les plus pertinents contiennent des mots similaires à ceux de la requête

#### Similarité de vecteurs:
- cosinus
- distance euclidienne
- Jaccard

#### Poids des termes:
- poids naif:
  - poids binaire (1 si terme présent, 0 si non) ==> distance de Jaccard
  - fréquence du mot dans le document (tf) ==> coefficient de Jaccard généralisé 
- poids plus pertinents:
  - on utilise des fonctions correctrices de la fréquence 
    - tf
    - 1+log(tf)
  - on prend aussi en compte la distribution du terme dans l'ensemble de la collection
	  - tf.idf

### Indexation sémantique latente (LSI)
une matrice qui décrit l'occurrence de certains termes dans les documents, et on transforme la matrice des occurrences en une «relation» entre les termes et des «concepts», et une relation entre ces concepts et les documents. On peut donc relier des documents entre eux.  
projection des requêtes et des documents dans un espace avec des composantes sémantiques:
- les meilleurs termes cooccurrents sont projetés sur les mêmes composantes
- les termes non-cooccurrents sont projetés sur des composantes différentes

Principe de l'indexation sémantique. indexation basée sur des concepts abstraits et non sur des termes:
- un concept abstrait est défini par plusieurs termes (permet de gérer la synonymie)
- un terme peut exprimer plusieurs concepts abstraits (permet de gérer la polysémie)  
LSI : une alternative au modèle standard par espaces vectoriels et mesure des poids par TF.IDF

#### Co-occurrence.
la cooccurrence est le fait que deux termes apparaissent dans les mêmes documents plus souvent que deux termes tirés aléatoirement.
deux termes ayant une relation forte de cooccurrence ont une forte chance d'être reliés sémantiquement.

### Segmentation de discours
parfois, l'information est contenue dans une petite partie seulement du document
méthode:
- découper le texte en différentes uniés (sous-séquences de mots du texte d'origine)
- repérer les points de changement de vocabulaire d'un sous-thème à un autre

chaque bloc est représenté par un vecteur dans l'espace des termes.  
exemple de pondération usuelle : la fréquence des termes à l'intérieur du bloc (sans IDF).  
cohésion = mesure de similarité entre deux blocs (cosinus des vecteurs).

## Rérérences
Cours sur le Traitement automatique du language naturel (TAL):  
[Cours 1](http://igm.univ-mlv.fr/ens/Master/M2/2007-2008/TAL/cours/mstal-1-1-m2.pdf); [Cours 2](http://igm.univ-mlv.fr/ens/Master/M2/2007-2008/TAL/cours/mstal-1-2-m2.pdf); [Cours 3](http://igm.univ-mlv.fr/ens/Master/M2/2007-2008/TAL/cours/mstal-1-3-m2.pdf).  
Pages Wikipédia sur les différents modèles de fouilles de texte:  
[Modèle Booléen](http://fr.wikipedia.org/wiki/Modèle_booléen); [Modèle Vectorielle](http://fr.wikipedia.org/wiki/Modèle_vectoriel); [Indéxation Sémantique Latente (LSI)](http://fr.wikipedia.org/wiki/Analyse_sémantique_latente).

# Spécifications algorithmiques et pratiques
***
## Design Pattern Strategy
Je pense que serait bien qu'on utilise le design pattern **Strategy** pour chaque parties.  
Petit rappel : **Strategy** est un patron de type comportemental grâce auquel des algorithmes peuvent être sélectionnés à la volée au cours du temps d'exécution selon certaines conditions (Merci Wikipédia).  
Le but est donc de définir un objet pour chaque partie (parser, database, statistiques), qui comportera toutes les méthodes et objets nécessaires a son bon fonctionnement, et certains objets de type abstrait. Ces objets définiront de façon abstraite toutes les méthodes qu'on voudra faire passer dans **Strategy**.

### Architecture projet
![archi](Structure.png)

## Config
Pour utiliser de façon optimum le design pattern **Strategy**, il faudrait créer un fichier de configuration qui décrirait quel stratégie utiliser à chaque étape du projet. Qui serait lu pour automatiquement à la création des obejts qui utilise des algorithmes **Strategy**. Mais qui servirai aussi pour d'autre variable statique utile.

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

## Tools
Répartition du travail à travers les outils de GitHub.
### Minestones and Issues
Les **Minestones** (Étapes) et **Issues** (Problèmes/Questions) sont un moyen simple de rapporter et diviser entre les contributeurs. Les contributeurs créé les **Milestones** qui servent d'étapes importantes du développement du projet (ex: "développer la Stratégie en charge du modèle de vectorielle de TF.IDF"). Ensuite les contributeurs rapporte toutes les **Issues** nécessaires à la réalisation de cette étape, que ce soit pendant le développement, la correction ou l'amélioration, et peuvent l'attribuer à des contributeurs en particulier. 
### Wiki
GitHub permet de maintenir un Wiki en rapport avec le projet. On l'utilisera comme documentation du projet, il contiendra:
- le manuel d'instalation
- le manuel d'utilisation
- la documentation du code
- et tout ce qui sera jugés utiles.

***
#Copyright and License
Copyright © 2014 Victor OUDIN <viktor.odex@gmail.com>  
Copyright © 2014 Lala Tiana RANDRIAMPARANY <thinas4@gmail.com>  
Copyright © 2014 Isabelle RICHARD <isabelle.richard89@gmail.com>  

EbookMining is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

EbookMining is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with EbookMining.  If not, see <http://www.gnu.org/licenses/>.

![GPLv3](http://www.gnu.org/graphics/gplv3-88x31.png)

