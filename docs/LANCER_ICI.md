# 🚀 Guide Rapide : Lancer les Comparaisons

## 📋 Prérequis

Installez matplotlib pour les graphiques :
```bash
pip install matplotlib
```

## 🎯 Commandes à Exécuter

### Option 1 : Script AVEC Graphiques (RECOMMANDÉ) 📊

```bash
# Se placer dans le dossier du projet
cd c:\Users\axelp\.gemini\antigravity\playground\outer-juno

# Lancer sur une petite instance (17 villes)
python compare_with_plots.py instances/17.in

# Lancer sur une instance moyenne (100 villes)
python compare_with_plots.py instances/100.in

# Avec timeout personnalisé
python compare_with_plots.py instances/51.in --timeout 120
```

**Ce script génère automatiquement 4 graphiques** :
1. `*_costs.png` - Barres comparant les coûts
2. `*_times.png` - Barres comparant les temps
3. `*_gaps.png` - Écart à la meilleure solution (%)
4. `*_tradeoff.png` - Compromis qualité/temps (scatter plot)

Les graphiques sont sauvegardés dans le dossier `results/`

### Option 2 : Script SANS Graphiques (plus simple)

```bash
# Juste voir les résultats en console
python compare_algorithms.py instances/17.in

# Avec export LaTeX
python compare_algorithms.py instances/17.in --latex-output table_17.tex
```

## 📊 Exemple de Résultat Console

```
================================================================================
Comparaison des algorithmes sur: instances/17.in
================================================================================

Instance chargée: 17 villes

1. Algorithme Exact (Branch & Bound)...
   Timeout: 60s
   Statut: completed
   Coût: 2094
   Temps: 35.234s

2. Heuristique Constructive (Nearest Neighbor)...
   Coût: 2187
   Temps: 0.001s

3. Recherche Locale (2-Opt après Nearest Neighbor)...
   Coût: 2181
   Temps: 0.015s

4. Méta-heuristique (GRASP, 50 itérations, alpha=0.2)...
   Coût: 2090
   Temps: 1.825s

================================================================================
📊 RÉSUMÉ DE LA COMPARAISON
================================================================================

Algorithme                Coût            Temps (s)    Gap (%)    Statut
--------------------------------------------------------------------------------
Exact (B&B)              2094            35.234       +0.19%     completed
Constructive (NN)        2187            0.001        +4.64%     completed
Local Search (2-Opt)     2181            0.015        +4.35%     completed
🏆 GRASP                 2090            1.825        0.00%      completed

================================================================================
Instance: instances/17.in (17 villes)
================================================================================

🎨 4 graphiques créés dans le dossier 'results/'

✨ Analyse terminée avec succès!
📊 Consultez les graphiques dans le dossier 'results/'
💡 Vous pouvez intégrer ces images dans votre rapport LaTeX
```

## 🖼️ Graphiques Générés

Les 4 PNG créés sont **haute résolution (300 dpi)** et prêts pour votre rapport LaTeX !

### Dans votre rapport LaTeX, ajoutez :

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{results/17_costs.png}
\caption{Comparaison des coûts sur l'instance 17.in}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{results/17_times.png}
\caption{Comparaison des temps d'exécution}
\end{figure}
```

## ⚡ Workflow Complet Recommandé

```bash
# 1. Tester sur une petite instance
python compare_with_plots.py instances/17.in

# 2. Tester sur plusieurs tailles
python compare_with_plots.py instances/51.in
python compare_with_plots.py instances/100.in
python compare_with_plots.py instances/280.in

# 3. Tous les graphiques sont dans results/
# Vous avez maintenant :
# - 17_costs.png, 17_times.png, 17_gaps.png, 17_tradeoff.png
# - 51_costs.png, 51_times.png, 51_gaps.png, 51_tradeoff.png
# - etc.

# 4. Intégrez-les dans rapport_tsp.tex
# 5. Compilez le PDF
pdflatex rapport_tsp.tex
```

## 🎨 Personnaliser les Graphiques

**Changer le dossier de sortie** :
```bash
python compare_with_plots.py instances/17.in --output-dir mes_graphiques
```

**Modifier les paramètres GRASP** :
```bash
python compare_with_plots.py instances/100.in --grasp-iterations 100 --grasp-alpha 0.3
```

## 🔧 Dépannage

**Erreur "matplotlib not found"** :
```bash
pip install matplotlib
```

**Erreur "No module named 'src'"** :
→ Assurez-vous d'être dans le bon dossier :
```bash
cd c:\Users\axelp\.gemini\antigravity\playground\outer-juno
```

**Les graphiques ne s'affichent pas** :
→ C'est normal ! Ils sont sauvegardés directement en PNG dans `results/`
→ Ouvrez le dossier `results/` pour les voir

**Timeout sur Branch & Bound** :
→ Augmentez le timeout :
```bash
python compare_with_plots.py instances/20.in --timeout 300
```

## 📝 Pour votre Rapport

1. **Lancez les comparaisons** sur 3-4 instances clés :
   - Une petite (17 villes)
   - Une moyenne (100 villes)
   - Une grande (500+ villes)

2. **Récupérez les graphiques** dans `results/`

3. **Intégrez dans le rapport LaTeX** en décommentant les lignes `\includegraphics`

4. **Compilez le PDF** :
   ```bash
   pdflatex rapport_tsp.tex
   pdflatex rapport_tsp.tex
   ```

---

**Astuce Pro** : Gardez la console ouverte pour copier les statistiques dans votre rapport ! 📋
