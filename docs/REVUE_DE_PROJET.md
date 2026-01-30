# Revue de Projet Finale

**Date** : 30 janvier 2026

## Synthèse

Ce document atteste de la finalisation du projet d'optimisation portant sur la résolution du Problème du Voyageur de Commerce (TSP). L'ensemble des objectifs fixés par le cahier des charges a été atteint.

## Livrables

### 1. Rapport Technique
Le fichier `Projet_d_Optimisation.pdf` constitue le livrable principal. Il contient :
- Une description détaillée des quatre algorithmes implémentés (Branch & Bound, Nearest Neighbor, 2-Opt, GRASP).
- Une analyse de la complexité théorique et pratique.
- Une campagne de tests sur 11 instances de tailles variées (17 à 1379 villes).
- Une analyse comparative des performances (Temps de calcul vs Qualité des solutions).

### 2. Code Source
L'implémentation est structurée de manière modulaire dans le répertoire `src/` :
- `model/` : Structures de données.
- `constructive/` : Heuristiques constructives.
- `local_search/` : Algorithmes d'amélioration locale.
- `exact/` : Méthodes exactes.
- `grasp/` : Méta-heuristiques.

### 3. Résultats Expérimentaux
Les données brutes et les visualisations sont disponibles dans le répertoire `report/`. Les métriques de stabilité pour les méta-heuristiques ont été validées (coefficient de variation < 1%).

## Conclusion

Le projet est complet, testé et documenté conformément aux exigences académiques du Master 2.
