# Rapport - Questions 1 à 4

Ce document détaille les réponses aux premières questions du projet, couvrant la modélisation et les trois premiers algorithmes implémentés.

## Question 1 : Modélisation et Chargement des Données

**Implémentation :** `src/model/tsp_model.py`

Le problème du Voyageur de Commerce (TSP) est modélisé par la classe `TSPInstance`.
*   **Format d'entrée** : Les fichiers d'instance (`.in`) contiennent sur la première ligne le nombre de villes `N`, suivi de la matrice de distance complète (N x N) sous forme d'une série d'entiers.
*   **Structure de données** :
    *   `experiments` : Matrice d'adjacence `matrix[i][j]` stockant la distance entre la ville `i` et la ville `j`.
    *   `n` : Nombre de villes.
*   **Solution** : La classe `Solution` stocke la liste ordonnée des villes visitées (`tour`) et le coût total associé (`cost`).

## Question 2 : Méthode Exacte (Branch and Bound)

**Implémentation :** `src/exact/branch_and_bound.py`

### Algorithme
Nous utilisons une approche par séparation et évaluation (Branch and Bound).
1.  **Solution Initiale** : On utilise l'heuristique du plus proche voisin pour obtenir une première borne supérieure (Upper Bound).
2.  **Exploration (Branch)** : On explore l'arbre des permutations des villes par un parcours en profondeur (DFS).
3.  **Évaluation (Bound)** : À chaque nœud, on calcule une borne inférieure (Lower Bound) du coût final pour la branche courante.
    *   *Lower Bound* = Coût du chemin actuel + Coût de l'Arbre Couvrant Minimum (MST) des villes non visitées + Connexion au chemin et au départ.
4.  **Élagage** : Si `LowerBound >= UpperBound`, on coupe la branche (elle ne peut pas contenir de meilleure solution).

### Complexité
*   **Théorique** : O(n!) (pire cas).
*   **Pratique** : Efficace pour n <= 20. Au-delà, le temps d'exécution explose exponentiellement.

## Question 3 : Heuristique Constructive (Nearest Neighbor)

**Implémentation :** `src/constructive/nearest_neighbor.py`

### Algorithme
C'est une méthode gloutonne (Greedy).
1.  On part d'une ville de départ arbitraire (0).
2.  Tant qu'il reste des villes à visiter :
    *   On choisit la ville non visitée la plus proche de la ville courante.
    *   On se déplace vers cette ville.
3.  On retourne à la ville de départ pour fermer la boucle.

### Complexité
*   **Temporelle** : **O(n²)**. Pour chaque ville (n étapes), on cherche le minimum parmi les restantes (n itérations).
*   **Qualité** : Donne rapidement une solution réalisable, mais souvent éloignée de l'optimal (+15-25% en moyenne).

## Question 4 : Recherche Locale (2-Opt)

**Implémentation :** `src/local_search/two_opt.py`

### Algorithme
L'algorithme cherche à améliorer une solution existante (issue de l'heuristique constructive) en supprimant les croisements (arêtes sécantes).
1.  On parcourt toutes les paires d'arêtes non-adjacentes dans le tour.
2.  Si échanger ces deux arêtes réduit la distance totale (détricotage d'un croisement), on effectue l'échange (swap).
3.  On répète le processus tant qu'une amélioration est trouvée (Best Improvement ou First Improvement).

### Complexité
*   **Temporelle** : **O(n²)** par itération de vérification. Le nombre total d'itérations pour atteindre un optimum local varie, mais la complexité empirique est souvent proche de **O(n³)**.
*   **Qualité** : Améliore significativement la solution constructive, mais reste sujette aux minima locaux.

---

**Note sur les Expériences (Q6)**
Les performances de ces trois méthodes (Exact, Constructive, Local Search) sont comparées graphiquement et analysées en détail dans le cadre de la **Question 6** (voir `Rapport_Q6_Final.md` et les graphiques associés).
