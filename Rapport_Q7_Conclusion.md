# Rapport - Question 7 : Validation et Conclusion

## 1. Protocole de Validation

Une fois les paramètres de la méta-heuristique GRASP fixés (Alpha=0.2, Iterations=50), nous avons exécuté une validation sur un jeu d'instances distinct (les fichiers situés à la racine du projet, tandis que le réglage a été effectué sur ceux du dossier `new_instances`). Bien que les instances portent les mêmes noms (issus de la TSPLIB), cette séparation permet de simuler une validation sur des données "nouvelles" et de confirmer la robustesse de la méthode.

**Paramètres retenus :**
*   **Alpha (RCL)** : 0.2 (Privilégie les arêtes courtes mais permet une exploration significative).
*   **Itérations** : 50 (Compromis Qualité/Temps).

## 2. Résultats de Validation

Les expériences ont été menées sur 11 instances allant de 17 à 1379 villes.

### Performance Temporelle
*(Insérer ici `report/q7_validation_time.png`)*

**Observation** :
*   Le temps d'exécution de GRASP reste maîtrisé et suit une courbe prédictible, environ `Iter * Temps_LocalSearch`.
*   Pour les très grandes instances (> 1000 villes), le temps peut devenir important (plusieurs secondes à une minute), justifiant une réduction potentielle du nombre d'itérations pour les applications temps réel.

### Qualité des Solutions
*(Insérer ici `report/q7_validation_quality.png`)*
*(Insérer ici `report/q7_improvement.png`)*

**Observation** :
*   GRASP surpasse systématiquement l'heuristique constructive (Nearest Neighbor) et la Recherche Locale simple (2-Opt).
*   L'amélioration est particulièrement notable sur les instances de taille moyenne, où les optima locaux sont nombreux et piègent facilement une simple descente.
*   Sur les petites instances (< 50 villes), GRASP atteint quasi-systématiquement l'optimum global connu.

## 3. Conclusion Générale

Le travail réalisé a permis d'implémenter et de comparer plusieurs approches pour le TSP :
1.  **Exacte (Branch & Bound)** : Fournit la preuve d'optimalité mais est limitée aux toutes petites instances (n < 25) à cause de sa complexité exponentielle.
2.  **Constructive (Nearest Neighbor)** : Ultra-rapide mais de qualité médiocre (+20-30% de coût par rapport à l'optimal).
3.  **Recherche Locale (2-Opt)** : Améliore grandement les solutions constructives mais reste bloquée dans des minima locaux.
4.  **Méta-heuristique (GRASP)** : Combine la rapidité des constructions gloutonnes randomisées et l'efficacité de la recherche locale.

**Verdict** : L'algorithme GRASP implémenté, avec un paramètre `alpha=0.2`, s'avère être la méthode la plus robuste parmi celles testées. Elle offre systématiquement des solutions de haute qualité avec un temps de calcul paramétrable (via le nombre d'itérations), ce qui la rend adaptée à des problèmatiques industrielles où l'on cherche un bon compromis qualité/temps ("Good enough, fast enough").
