# Des données aux commandes : mon premier dashboard avec Dash

**Anella Manari — E4, Data Science & Intelligence Artificielle — ESIEE Paris**

Ce projet a été réalisé dans le cadre du cours de Python 2, à partir du chapitre consacré aux dashboards. L’objectif était de construire progressivement une application qui permet d’explorer des données, de choisir une année et de suivre leur évolution grâce à une animation.

## Le point de départ

Un graphique Plotly permet déjà de zoomer et d’afficher des informations au survol. Avec Dash, j’ai appris à ajouter des commandes qui déclenchent du code Python pour modifier les données affichées.

L’application utilise le jeu de données **Gapminder**, fourni avec Plotly Express. Il contient notamment la population, le PIB par habitant et l’espérance de vie de différents pays, de 1952 à 2007, tous les cinq ans.

Dans le graphique :

- chaque bulle représente un pays ;
- l’axe horizontal correspond au PIB par habitant ;
- l’axe vertical correspond à l’espérance de vie ;
- la couleur indique le continent ;
- la taille de la bulle représente la population.

## Préparer le projet

J’ai créé un projet sans package et installé ses dépendances avec uv :

    uv init --no-package
    uv sync
    uv add dash plotly pandas

Au moment de l’installation, j’ai rencontré un premier problème : mon projet s’appelait `dash`, comme la bibliothèque à installer. uv refusait cette dépendance, car cela revenait à demander au projet de dépendre de lui-même.

J’ai remplacé le nom du projet par `projet-dash` dans `pyproject.toml`, puis relancé l’installation. Le dossier a conservé son nom initial.

## Une application construite en quatre étapes

### 1. Afficher un premier graphique — `dash_01.py`

J’ai commencé par afficher les données de 2002 dans une page contenant un titre, un graphique et un texte explicatif.

Cette première version m’a permis de distinguer les rôles des deux outils : **Plotly construit la figure et Dash organise son affichage dans la page**.

J’ai également testé le survol des bulles, le zoom et le masquage des continents depuis la légende. L’année restait fixe dans le code.

### 2. Relier un menu au graphique — `dash_02.py`

J’ai ensuite ajouté un menu déroulant pour choisir l’année.

Cette version répond aux deux premiers exercices orange :

**Décorateurs :** le graphique, le titre et la description sont actualisés ensemble grâce à un callback. Chaque élément possède un identifiant permettant à Dash de le retrouver.

**Drop down :** les choix du menu sont construits automatiquement à partir des années présentes dans le tableau. Je n’ai donc pas besoin d’écrire chaque année manuellement.

Le callback reçoit une année et renvoie trois résultats, dans le même ordre que les sorties déclarées : la figure, le titre et la description.

### 3. Remplacer le menu par un curseur — `dash_03.py`

Pour l’exercice « Slider », j’ai remplacé le menu déroulant par un curseur.

Les graduations sont générées à partir des années disponibles. Le paramètre `step=None` limite la sélection à ces années : l’utilisateur ne peut pas choisir une année pour laquelle le tableau ne contient aucune donnée.

La fonction de mise à jour reste la même. Seul le composant qui lui transmet l’année change.

### 4. Faire défiler les années — `dash_04.py`

La dernière version ajoute une animation et les boutons **Play/Pause**.

Un composant `dcc.Interval` déclenche régulièrement un callback qui fait avancer le curseur. Le changement du curseur provoque ensuite la mise à jour du graphique et des textes.

L’animation démarre en pause :

- **Play** active le minuteur ;
- **Pause** le désactive ;
- après 2007, le défilement reprend en 1952.

Pour revenir à la première année après la dernière, j’utilise le modulo. L’année actuelle est récupérée avec `State`, ce qui permet de reprendre le défilement depuis la position du curseur.

J’ai aussi ajouté le complément proposé dans le cours : un menu pour choisir une vitesse lente, normale ou rapide. Il modifie le délai du minuteur, exprimé en millisecondes.

## Ce que j’ai compris des callbacks

Le `layout` décrit les éléments présents sur la page. Les callbacks définissent leurs réactions.

Dans cette application :

- `Input` surveille une propriété qui déclenche une mise à jour ;
- `Output` désigne la propriété à modifier ;
- `State` permet de lire une valeur sans déclencher la fonction lorsqu’elle change.

Par exemple, choisir une année déclenche une fonction Python qui prépare une nouvelle figure. Dash utilise ensuite le résultat pour actualiser la page.

## Quelques points qui m’ont demandé de l’attention

**Lancer le bon fichier.** Au début, les deux premières versions semblaient identiques : le serveur de la première version était encore lancé. J’ai arrêté le programme avec `Ctrl + C`, lancé le fichier voulu et actualisé le navigateur.

**Adapter les exemples du cours.** Le cours utilise une ancienne version de Dash. J’ai utilisé les imports actuels depuis `dash` et la commande `app.run(debug=True)`. Les boutons sont créés avec `html.Button`.

**Respecter l’ordre des sorties.** Lorsqu’un callback modifie plusieurs éléments, les valeurs renvoyées doivent correspondre au nombre et à l’ordre des `Output`.

## Lancer le projet

Depuis le dossier du projet :

    uv sync
    uv run python dash_04.py

Ouvrir ensuite cette adresse dans un navigateur :

http://127.0.0.1:8050/

Le terminal doit rester ouvert pendant l’utilisation. Pour arrêter le serveur, utiliser `Ctrl + C`.

Les autres étapes peuvent être lancées séparément en remplaçant le nom du fichier par `dash_01.py`, `dash_02.py` ou `dash_03.py`. Il faut arrêter le serveur précédent avant de lancer une autre version sur le même port.

## Bilan

Ce TP m’a permis de passer d’un graphique affichant une année fixe à une application pilotée par l’utilisateur.

Le point que je retiens surtout est qu’une interaction peut en entraîner plusieurs : le minuteur change le curseur, puis le curseur fait changer le graphique et les textes. Garder les différentes versions m’a aidée à comprendre chaque ajout avant de passer au suivant.

## Ressource du cours

[Les dashboards — Python 2, D. Courivaud, ESIEE Paris](https://perso.esiee.fr/~courivad/courses/E4-DSIA-FD-Python-2/sources/python-28-dash.html)