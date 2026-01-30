# Guide d'Utilisation du Projet

Ce document détaille la procédure pour exécuter les algorithmes de résolution du TSP et reproduire les résultats présentés dans le rapport.

## Installation de l'Environnement

Le projet nécessite un interpréteur Python 3 ainsi que quelques bibliothèques standards pour le calcul scientifique et la visualisation.

1.  **Cloner ou télécharger le projet** dans votre environnement de travail.
2.  **Installer les dépendances** nécessaires via pip :

```bash
pip install pandas matplotlib
```

## Exécution des Algorithmes

Le projet dispose d'un script principal `benchmark.py` conçu pour automatiser l'exécution des tests.

### Lancement du Benchmark Complet

Pour exécuter tous les algorithmes (Exact, Constructif, Recherche Locale, GRASP) sur toutes les instances disponibles dans le dossier `instances/` :

```bash
python benchmark.py
```

**Note sur le temps d'exécution** :
*   L'algorithme **Exact** (Branch & Bound) dispose d'une limite de temps (timeout) fixée à 60 secondes. Il ne sera exécuté que sur les petites instances ($N \le 20$) pour éviter une explosion combinatoire.
*   Les heuristiques (Nearest Neighbor, 2-Opt, GRASP) seront exécutées sur toutes les instances.

### Sortie et Résultats

Les résultats de l'exécution seront automatiquement sauvegardés dans le dossier `report/`. Vous y trouverez :

*   `benchmark_results.csv` : Un fichier CSV contenant les temps d'exécution et les coûts des solutions pour chaque algorithme et chaque instance.
*   Les graphiques de performance (format PNG) :
    *   Analyse de la complexité temporelle.
    *   Comparaison de la qualité des solutions.
    *   Analyse des écarts (gaps) par rapport à la meilleure solution connue.

## Compilation du Rapport

Le rapport technique est rédigé en LaTeX. Le fichier source `rapport_final.tex` se trouve à la racine (ou dans `report/` selon la version).

Pour générer le PDF :
1.  Assurez-vous d'avoir une distribution LaTeX installée (MiKTeX, TeX Live).
2.  Compilez le fichier `.tex` :

```bash
pdflatex report/rapport_final.tex
```

Le fichier PDF final `Projet_d_Optimisation.pdf` est également fourni à la racine du projet prêt à la lecture.
