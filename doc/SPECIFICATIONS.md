Insertion d'un e-book:
1. parser l'e-book;
2. le nettoyer (enlever la ponctuation et autre);
3. compter le nombre de mots dans l'e-book;
4. enlever les mots les plus courants de la langue française (mais, ou, et, donc, or, ni, car, ...);
5. compter le nombre d'occurrence des mots;
6. enlever le genre et le nombre des mots;
7. calculer le TF des mots;
8. entrer le livre, ses mots et leur TF dans la base de données.
Vecteur de TF-IDF d'un e-book:
1. récupérer le nombre de livres dans la base;
2. calculer l'IDF de chaque mot de la base;
3. extraire les TF de l'e-book;
4. construire le vecteur de TF-IDF.
Matrice de similarité:
1. Pour chaque paire d'e-book, calculer la similarité cosinus;
2. enregistrer le résultat dans la matrice symétrique.
Recommandation:
1. choix d'un ou plusieurs e-books par l'utilisateur;
2. copie de la (les) lignes(s) de la matrice de similarité du (des) e-book(s);
3. dans le cas de plusieurs e-books, additionner les similarités, trier par ordre décroissant de similarité;
4. recommander des livres, du plus similaire au moins similaire.

Options possibles :
Langue :
Offrir la possibilité, lors de la création et de l'ajout de livres à la base de données, de choisir la langue du corpus, en l'entrant en paramètre. Ensuite, ce paramètre serait utilisé lors de l'élimination des mots les plus courants de la langue choisie, et de la suppression du genre et du nombre.

Similarité :
Offrir la possibilité, lors du calcul de similarité, de choisir le type de similarité à utiliser (cosinus, euclidienne, ...)

Augmentation de la vitesse d'accès à la base :
Actuellement, les écritures dans la base sont séquentielles, ce qui ralentit l'ajout de livres à la base, l'ajout simultané de plusieurs livres n'étant pas possible. En rendant ces accès atomiques et asynchrones, en utilisant un SGBD (système de gestion de base de données), il serait alors possible de paralléliser les écritures et lectures, augmentant considérablement la vitesse d'ajout de livres à la base de données et le calcul des TF-IDF.

