# Rapport - Problème du Voyageur de Commerce (TSP)

## 1. Situations réelles modélisables comme un TSP

Le TSP apparaît dans de nombreux domaines au-delà de la simple planification d'itinéraires :
*   **Perçage de circuits imprimés (PCB)** : Minimiser le temps de déplacement de la tête de perçage pour faire des trous à différents endroits d'une carte électronique.
*   **Séquençage de génome** : Reconstruire une séquence d'ADN à partir de fragments en minimisant les chevauchements ou les distances d'édition.
*   **Optimisation de tournées de livraison/collecte** : Le classique problème de logistique pour FedEx, UPS, ou la collecte des déchets.
*   **Observation astronomique** : Minimiser le mouvement d'un télescope pour observer une liste d'étoiles.

## 2. Algorithme Exact : Branch and Bound

### Description
L'algorithme de Branch and Bound (Séparation et Évaluation) explore l'arbre des solutions possibles de manière intelligente.
*   **Séparation (Branching)** : On divise le problème en sous-problèmes, par exemple en fixant la prochaine ville à visiter.
*   **Évaluation (Bounding)** : Pour chaque sous-problème (noeud de l'arbre), on calcule une borne inférieure (Lower Bound) du coût. Si le chemin partiel actuel + la borne inférieure est déjà pire que la meilleure solution complète trouvée jusqu'ici (Upper Bound), on "coupe" (prune) cette branche car elle ne peut pas contenir l'optimum.
*   **Implémentation** : Nous avons utilisé un parcours en profondeur (DFS) avec une borne simple.

### Complexité
*   Théorique : O(n!) car dans le pire des cas, on doit explorer toutes les permutations.
*   En pratique : Très dépendant de la qualité de la borne inférieure.

### Cas pathologiques
*   Les graphes où toutes les arêtes ont des poids similaires ou identiques. La borne inférieure devient peu discriminante et l'élagage est inefficace, forçant une exploration quasi-totale.

## 3. Heuristique Constructive : Plus Proche Voisin

### Description
On part d'une ville de départ arbitraire. À chaque étape, on choisit la ville non visitée la plus proche de la ville courante. On répète jusqu'à visiter toutes les villes, puis on retourne au départ.

### Complexité
*   O(n²) : À chaque étape (n étapes), on cherche le minimum parmi les villes restantes (O(n)).

### Cas pathologiques
*   Graphes où choisir le plus proche voisin mène à une impasse ou force une arête finale très longue pour fermer la boucle ("peigner dans un coin"). La solution peut être arbitrairement mauvaise par rapport à l'optimum.

## 4. Heuristique de Recherche Locale : 2-opt

### Description
On part d'une solution (tournée) existante. On essaie d'améliorer cette solution en supprimant deux arêtes et en reconnectant les chemins différemment pour réduire la distance totale (décroisement). On répète tant qu'une amélioration est possible.

### Complexité
*   Chaque itération teste O(n²) paires d'arêtes. Le nombre d'itérations peut varier, mais en pratique c'est rapide.
*   Pire cas théorique exponentiel pour atteindre l'optimum local, mais polynomial en pratique pour une bonne amélioration.

### Cas pathologiques
*   Minimums locaux : L'algorithme se bloque dans une solution "bonne" mais pas optimale, sans pouvoir en sortir par de simples échanges 2-opt.

## 5. Méta-heuristique : GRASP

### Description
GRASP (Greedy Randomized Adaptive Search Procedure) combine construction aléatoire et recherche locale.
*   **Phase 1 (Construction)** : On construit une solution gloutonne mais randomisée. Au lieu de prendre systématiquement le meilleur voisin, on constitue une Liste Restreinte de Candidats (RCL) contenant les meilleurs choix (définis par un paramètre alpha), et on tire au sort parmi eux.
*   **Phase 2 (Recherche Locale)** : On applique 2-opt sur la solution construite pour atteindre un optimum local.
*   On répète ces deux phases un nombre d'itérations donné et on garde la meilleure solution globale.

### Choix des paramètres
*   **Alpha = 0.2** : Compromis entre pur glouton (alpha=0) et pur aléatoire (alpha=1). Permet de la diversité sans choisir des arêtes trop mauvaises.
*   **Itérations** : Fixé à 20-50 pour les tests afin de limiter le temps de calcul tout en explorant plusieurs bassins d'attraction.

### Complexité
*   O(k * (n² + Complexité(LocalSearch))), où k est le nombre d'itérations.

### Cas pathologiques
*   Comme 2-opt, GRASP peut peiner si l'espace de recherche est très accidenté avec des bassins d'attraction profonds mais sous-optimaux difficiles à échapper avec une simple randomisation constructive.

## 6. Résultats Expérimentaux

Les tests ont été effectués sur différentes instances (`.in`).
L'algorithme exact a été limité à 60 secondes.

| Instance | Taille (N) | Constructive (Coût) | Local Search (Coût) | GRASP (Coût) | Exact (Coût/Temps) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 17.in | 17 | 2187 | 2181 | 2090 | 2094 (60s - Timeout, sol partielle/subopt) |
| 51.in | 51 | 511 | 441 | 441 | N/A |
| 52.in | 52 | 8980 | 8287 | 8181 | N/A |
| 101.in | 101 | 803 | 679 | 685 | N/A |
| 100.in | 100 | 27807 | 23951 | 23010 | N/A |
| 127.in | 127 | 135737 | 123755 | 127663 | N/A |
| 280.in | 280 | 3157 | 2835 | 2991 | N/A |
| 439.in | 439 | 131281 | 117378 | 122102 | N/A |
| 654.in | 654 | 43457 | 35814 | 35958 | N/A |
| 783.in | 783 | 11054 | 9587 | 10245 | N/A |
| 1379.in | 1379 | 68964 | 61566 | 65355 | N/A |

**Analyse :**
1.  **Exact** : Ne passe pas à l'échelle. Pour N=17, il n'a pas prouvé l'optimalité en 60s (notre implémentation basique est lente). Le GRASP a même trouvé mieux (2090 vs 2094), ce qui montre que le B&B, s'il est interrompu, peut être pire qu'une bonne heuristique.
2.  **Constructive vs Local Search** : La recherche locale (2-opt) améliore systématiquement la solution constructive, souvent de manière significative (ex: 43457 -> 35814 pour 654.in).
3.  **GRASP** : GRASP fournit souvent des résultats compétitifs, parfois meilleurs que la simple recherche locale (ex: 2090 vs 2181 pour 17.in, 23010 vs 23951 pour 100.in), mais parfois légèrement moins bons si l'itération aléatoire n'a pas convergé vers le meilleur bassin en peu de temps. Son coût en temps est plus élevé.
4.  **Influence de la taille** : Pour les très grandes instances (1379.in), GRASP devient coûteux (31s pour 20 itérations), tandis que la recherche locale est plus rapide (0.9s) pour un résultat parfois meilleur.

En conclusion, pour de grandes instances, une bonne heuristique de recherche locale (ou un GRASP avec peu d'itérations) offre le meilleur compromis temps/qualité.
