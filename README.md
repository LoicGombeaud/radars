# Dataviz : radars pédagogiques de Bordeaux

Ce projet est disponible ici : [https://radars.loicgombeaud.com](https://radars.loicgombeaud.com)

## Motivation

Depuis quelques décennies, les rues ont changé de fonction : d'un lieu d'échange,
de convivialité, et de création de valeur, elles sont devenues des tuyaux à
véhicules motorisés, où l'humain peine à trouver sa place.

La majorité de l'espace est en effet dédié aux véhicules motorisés, que ce soit
pour leur circulation ou pour leur stationnement ; les piétons sont relégués
à des trottoirs souvent minuscules, et fréquemment envahis d'obstacles en tout
genre (poubelles, boitiers techniques, véhicules garés sauvagement, etc.).

Un des leviers pour inverser cette tendance est la réduction de la vitesse des 
véhicules motorisés : la vitesse tue ; la réduire, c'est rendre aux piétons le
droit de circuler en sécurité. Cela contribue également à leur confort en
réduisant le volume sonore des rues.

En 2022, la ville de Bordeaux a réduit la vitesse maximale autorisée dans la
grande majorité des rues, de 50 km/h à 30 km/h. Des panneaux "30" ont été
plantés un peu partout, des radars pédagogiques ont été installées ; mais les
conducteurs ont-ils vraiment adapté leur comportement en conséquence ?

Planter des petits panneaux, installer des radars inoffensifs, est-ce vraiment
suffisant ? Ou faut-il également modifier en profondeur le profil des rues, afin
de rendre physiquement impossible les dépassements de vitesse excessifs ?

Ce projet vise à répondre à ces deux questions, en présentant conjointement les
vitesses mesurées à différents endroits de la ville, et une photo de l'endroit
où ces mesures ont été effectuées.


## Architecture technique

Les quatres composants de ce projet sont les suivants :
- `etl` : ce module, dont le nom est issu de l'anglais "Extract, Transform, Load",
est exécuté une fois par jour, et se charge d'extraire les données brutes depuis
la plateforme d'Open Data de Bordeaux Métropole, de les transformer en statistiques
exploitables, puis de les charger dans la base de données interne du projet ; il
est codé en Python et utilise la librairie NumPy
- `back` : ce module expose une API REST, qui permet au front d'accéder simplement
à la base de données des statistiques journalières et horaires ; il est codé en
Python, avec le framework FastAPI
- `front` : partie visible de l'iceberg, le front présente les données visuellement,
plaçant les radars sur une carte pour permettre à chacun de consulter les vitesses
pratiquées dans son quartier ; il est codé en Vue.js 3 / Vite
- `deploy` : mécanisme de déploiement et mise à jour ; ce projet étant hébergé
sur un cluster Kubernetes, il s'agit d'un chart helm

## Reste à faire

Améliorations futures :
- (front) meilleur affichage sur mobile
- (front) explication de la motivation du projet
- (front, back) historique sur N jours
- (deploy) mise en place de CI/CD (par exemple GitHub Actions)
