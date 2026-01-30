# Projet d'Optimisation - Résolution du TSP

Ce projet s'inscrit dans le cadre du Master 2 Optimisation et vise à implémenter et comparer différentes approches algorithmiques pour la résolution du Problème du Voyageur de Commerce (Traveling Salesperson Problem).

## Structure du Projet

L'architecture du projet est organisée comme suit :

- **src/** : Contient l'ensemble du code source Python.
  - **model/** : Définition des classes de base (`TSPInstance`, `Solution`).
  - **constructive/** : Implémentation de l'heuristique constructive (Plus Proche Voisin).
  - **local_search/** : Implémentation de la recherche locale (2-Opt).
  - **grasp/** : Implémentation de la méta-heuristique GRASP.
  - **exact/** : Implémentation de la méthode exacte (Branch and Bound).
- **instances/** : Contient les jeux de données de test (format TSPLIB).
- **report/** : Contient les résultats d'exécution, les graphiques générés et le rapport LaTeX.
- **docs/** : Documentation technique complémentaire.
- **scripts/** : Scripts utilitaires secondaires.

Le rapport complet au format PDF est disponible à la racine : `Projet_d_Optimisation.pdf`.

## Utilisation

### Prérequis
- Python 3.8 ou supérieur
- Bibliothèques : `pandas`, `matplotlib`

### Exécution du Benchmark
Pour lancer la campagne de tests complète sur l'ensemble des instances :

```bash
python benchmark.py
```

Ce script exécutera séquentiellement les différents solveurs et générera les fichiers de résultats dans le dossier `report/`.

## Auteurs

- Lucas AUDIC
- Axel BATTEUX
- Romain PERIDY
- Tristan DELEPINE
