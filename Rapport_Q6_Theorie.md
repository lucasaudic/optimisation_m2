# Rapport - Question 6 : Analyse des Algorithmes

Ce document présente l'analyse détaillée des quatre méthodes implémentées : Branch & Bound (Exact), Nearest Neighbor (Constructive), 2-Opt (Recherche Locale) et GRASP.

## 1. Méthode Exacte : Branch and Bound

### Description (Pseudo-code)
```
Fonction BranchAndBound(instance, time_limit):
    SolutionInitiale = NearestNeighbor(instance)
    MeilleureSolution = SolutionInitiale
    BorneSupérieure = Coût(SolutionInitiale)
    
    DFS(noeud_courant, visités, coût_courant, chemin_courant):
        Si TempsImpartiEcoule(): Retourner
        
        Si coût_courant + LowerBound(non_visités) >= BorneSupérieure:
            Retourner (Élagage)
            
        Si ToutVisité():
            coût_total = coût_courant + Distance(noeud_courant, départ)
            Si coût_total < BorneSupérieure:
                BorneSupérieure = coût_total
                MeilleureSolution = chemin_courant
            Retourner

        Pour chaque ville v non visitée (triées par distance croissante):
            DFS(v, visités + {v}, coût_courant + Distance(noeud_courant, v), chemin_courant + {v})
```
*Note : La LowerBound utilisée est basée sur le MST des nœuds restants + les deux arêtes les plus courtes connectant ce MST au chemin courant et au départ.*

### Complexité Temporelle
*   **Pire cas** : O(n!) car il s'agit d'une exploration exhaustive de l'arbre des permutations dans le pire cas (si l'élagage est inefficace).
*   **En pratique** : Fortement dépendant de la qualité de la borne inférieure et de la solution initiale.

### Instances Pathologiques
*   Les instances où les coûts des arêtes sont très similaires (ou uniformes), rendant la borne inférieure peu discriminante (Low Bound GAP), ce qui empêche l'élagage efficace.
*   Graphes complets de grande taille (> 20 nœuds) où l'explosion combinatoire rend la méthode inutilisable en temps raisonnable.

---

## 2. Méthode Constructive : Nearest Neighbor

### Description (Pseudo-code)
```
Fonction NearestNeighbor(instance, ville_depart):
    NonVisités = Tous les noeuds sauf ville_depart
    Tour = [ville_depart]
    Courant = ville_depart
    
    Tant que NonVisités n'est pas vide:
        Prochain = Trouver v dans NonVisités minimisant Distance(Courant, v)
        Ajouter Prochain à Tour
        Retirer Prochain de NonVisités
        Courant = Prochain
        
    Retourner Tour (connecté au départ)
```

### Complexité Temporelle
*   À chaque étape, on cherche le minimum parmi `k` villes restantes.
*   Total : O(n) + O(n-1) + ... + O(1) = **O(n²)**.

### Instances Pathologiques
*   **Problème** : L'algorithme est "myope" (greedy). Il fait le meilleur choix local sans considérer les conséquences futures.
*   **Exemple** : Une ligne de villes avec le départ au milieu, ou forçant à prendre une arête très longue à la fin pour revenir au départ.
*   **Ratio d'approximation** : Dans le pire cas général, le ratio peut croître avec le nombre de sommets (O(log n) ou pire selon les variantes métriques/non métriques). Pour le TSP métrique, il peut être arbitrairement mauvais par rapport à l'optimal (borné par un facteur dépendant de n).

---

## 3. Méthode Recherche Locale : 2-Opt

### Description (Pseudo-code)
```
Fonction TwoOpt(instance, tour_initial):
    MeilleurTour = tour_initial
    Amélioration = Vrai
    
    Tant que Amélioration est Vrai:
        Amélioration = Faux
        Pour i de 1 à n-2:
            Pour j de i+1 à n-1:
                Si Gain(i, j) > 0:
                    // Gain = (dist(i-1, i) + dist(j, j+1)) - (dist(i-1, j) + dist(i, j+1))
                    Inverser le segment Tour[i...j]
                    Mettre à jour MeilleurTour
                    Amélioration = Vrai
                    
    Retourner MeilleurTour
```

### Complexité Temporelle
*   Une itération de recherche de mouvement (les deux boucles) prend **O(n²)**.
*   Le nombre d'améliorations peut être exponentiel dans le pire cas, mais en pratique on observe souvent un nombre d'itérations sub-quadratique ou linéaire. On considère souvent une complexité empirique proche de **O(n³)** ou **O(n²)** avec des optimisations.

### Instances Pathologiques
*   **Optima Locaux** : Le 2-opt peut rester bloqué dans un minimum local loin de l'optimal global.
*   **Exemple** : Structures croisées complexes nécessitant de déplacer 3 arêtes ou plus simultanément (que 2-opt ne voit pas) pour être améliorées.
*   Une solution peut être "2-optimale" (aucune amélioration 2-opt possible) tout en étant significativement moins bonne que la solution optimale.

---

## 4. Méta-heuristique : GRASP

### Description (Pseudo-code)
```
Fonction GRASP(instance, alpha, max_iterations):
    MeilleureGlobale = NULL
    
    Pour k de 1 à max_iterations:
        // Phase 1 : Construction
        TourCandidat = RandomizedGreedy(instance, alpha)
        
        // Phase 2 : Recherche Locale
        SolutionLocale = TwoOpt(instance, TourCandidat)
        
        Si Coût(SolutionLocale) < Coût(MeilleureGlobale):
            MeilleureGlobale = SolutionLocale
            
    Retourner MeilleureGlobale

Fonction RandomizedGreedy(instance, alpha):
    // ... (Sélection aléatoire parmi RCL = candidats <= min + alpha * (max-min))
```

### Complexité Temporelle
*   Construction : O(n²) par itération.
*   Recherche Locale : O(k * n²) ou empiriquement O(n³) par itération (où k est le nombre d'améliorations).
*   Total : **Iter * (O(n²) + O(LocalSearch))**.
*   GRASP est linéairement dépendant du nombre d'itérations (`max_iterations`).

### Instances Pathologiques
*   Instances où l'espace de recherche est "plat" ou chaotique, rendant la recherche locale inefficace peu importe le point de départ.
*   Instances "Needle in a haystack" où seules des configurations très spécifiques (difficiles à générer aléatoirement avec la construction gloutonne) mènent au bassin d'attraction de l'optimum global.

## 5. Expérimentations et Résultats

Pour générer les données comparatives :
1.  Assurez-vous que Python est accessible.
2.  Exécutez le script : `python benchmark_q6.py`
3.  Le fichier `report/benchmark_q6_results.csv` contiendra les temps et coûts.
4.  Utilisez ces données pour tracer les graphiques demandés (Temps vs Taille, Qualité vs Taille).

*Note : Les performances observées dépendront de la machine d'exécution.*
