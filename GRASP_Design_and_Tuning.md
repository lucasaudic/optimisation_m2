# Conception et Réglage de l'Algorithme GRASP

## 1. Description de l'Algorithme

L'algorithme GRASP (Greedy Randomized Adaptive Search Procedure) implémenté pour le problème du voyageur de commerce (TSP) se déroule en itérations successives. Chaque itération comprend deux phases :

### Phase 1 : Construction (Modification de l'Heuristique 3)
*   **Base** : L'heuristique du Plus Proche Voisin (Nearest Neighbor) décrite à la question 3.
*   **Modification** : Introduction de la randomisation via une Liste Restreinte de Candidats (RCL - Restricted Candidate List).
*   **Mécanisme** : 
    *   Au lieu de choisir systématiquement la ville la plus proche, l'algorithme identifie un ensemble de "bonnes" villes candidates (celles dont la distance est inférieure à un seuil `min + alpha * (max - min)`).
    *   La ville suivante est choisie aléatoirement parmi cette liste RCL.
    *   Le point de départ est également choisi aléatoirement à chaque itération.

### Phase 2 : Recherche Locale (Heuristique 4)
*   **Méthode** : Algorithme 2-opt (décrit à la question 4).
*   **Objectif** : Améliorer la solution construite en phase 1 en supprimant les croisements d'arêtes (décroisements).

## 2. Choix des Paramètres et Justification

### Paramètre Alpha (Seuil RCL)
*   **Rôle** : Contrôle l'équilibre entre gloutonnerie (Alpha=0) et pur hasard (Alpha=1).
*   **Protocole d'Expérience** :
    *   Script : `tune_grasp.py`
    *   Instances de Test : `51.in` (eil51) et `101.in` (eil101).
    *   Justification du choix des instances : Ces instances sont de taille moyenne, permettant une exécution rapide de nombreuses itérations pour le réglage, tout en étant assez complexes pour révéler les différences de performance entre les valeurs d'alpha.
    *   Valeurs testées : 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, ... 1.0.
    *   Critère de choix : Meilleur compromis entre le coût moyen et le meilleur coût trouvé sur plusieurs exécutions.

### Critère d'Arrêt
*   **Choix** : Nombre fixe d'itérations (`max_iterations`).
*   **Intervalles testés** : 20, 50, 100.
*   **Justification** : Un nombre fixe d'itérations permet de contrôler le temps de calcul tout en donnant à l'algorithme une chance suffisante d'explorer l'espace de recherche à partir de multiples points de départ différents. Pour les instances de taille moyenne, 50 itérations offrent généralement une bonne convergence sans temps excessif.

## 3. Instructions d'Exécution

Pour lancer le réglage des paramètres et générer les justifications expérimentales :

```bash
python tune_grasp.py
```

Pour résoudre une instance spécifique avec les paramètres retenus :

```bash
python solve.py instances/new_instances/51.in grasp
```
