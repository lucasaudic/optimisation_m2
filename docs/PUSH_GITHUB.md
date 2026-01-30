# 🚀 Guide pour Push vers GitHub

## ⚠️ Problème Détecté

Git n'est pas accessible dans votre terminal. Voici plusieurs solutions :

---

## 🎯 Solution 1 : Via GitHub Desktop (LE PLUS SIMPLE)

### Étapes :

1. **Ouvrez GitHub Desktop** (vous l'avez déjà installé !)
2. Cliquez sur **File → Add Local Repository**
3. Sélectionnez le dossier :
   ```
   c:\Users\axelp\.gemini\antigravity\playground\outer-juno
   ```
4. Si le dossier n'est pas un repository Git :
   - Cliquez sur **"create a repository"**
   - OU copiez les fichiers dans le dossier cloné de `optimisation_m2`

5. **Voir les changements** :
   - GitHub Desktop affichera tous les fichiers modifiés/ajoutés
   
6. **Commit** :
   - Cochez les fichiers importants :
     - ✅ `Projet_d_Optimisation.pdf`
     - ✅ `rapport_final.tex`
     - ✅ `compare_algorithms.py`
     - ✅ `compare_with_plots.py`
     - ✅ Les fichiers markdown de documentation
   - En bas à gauche, écrivez un message de commit :
     ```
     Ajout rapport final PDF avec graphiques et scripts de comparaison
     ```
   - Cliquez sur **"Commit to main"**

7. **Push** :
   - Cliquez sur **"Push origin"** en haut

✅ **C'est fait !**

---

## 🎯 Solution 2 : Installer Git et utiliser la ligne de commande

### Installer Git :

1. Téléchargez depuis : https://git-scm.com/download/win
2. Installez (acceptez toutes les options par défaut)
3. **Redémarrez votre terminal**

### Puis exécutez :

```powershell
cd c:\Users\axelp\.gemini\antigravity\playground\outer-juno

# Vérifier si c'est un repo Git
git status

# Si pas un repo, initialiser
git init
git remote add origin https://github.com/lucasaudic/optimisation_m2.git

# Ajouter les fichiers importants
git add Projet_d_Optimisation.pdf
git add rapport_final.tex
git add compare_algorithms.py
git add compare_with_plots.py
git add GUIDE_UTILISATION.md
git add LANCER_ICI.md
git add COMPILATION_GUIDE.md
git add STATUT_FINAL.md

# Commit
git commit -m "Ajout rapport final PDF avec graphiques et scripts de comparaison"

# Push
git push -u origin main
```

---

## 🎯 Solution 3 : Upload manuel via GitHub Web

1. Allez sur : https://github.com/lucasaudic/optimisation_m2
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur **"Add file"** → **"Upload files"**
4. Glissez-déposez ces fichiers :
   - `Projet_d_Optimisation.pdf` ⭐ (le plus important)
   - `rapport_final.tex`
   - `compare_algorithms.py`
   - `compare_with_plots.py`
   - Les guides markdown
5. Écrivez un message de commit
6. Cliquez sur **"Commit changes"**

---

## 📋 Fichiers à Push (Par Priorité)

### Essentiels ⭐⭐⭐
- `Projet_d_Optimisation.pdf` (rapport final)
- `rapport_final.tex` (source LaTeX)

### Très Importants ⭐⭐
- `compare_algorithms.py`
- `compare_with_plots.py`
- `rapport_tsp_overleaf.zip`

### Utiles ⭐
- `STATUT_FINAL.md`
- `GUIDE_UTILISATION.md`
- `LANCER_ICI.md`
- `COMPILATION_GUIDE.md`

### Optionnels
- Les autres fichiers markdown
- Les scripts supplémentaires

---

## ⚠️ ATTENTION

**Vérifiez que vous avez les droits** sur le repository `lucasaudic/optimisation_m2` !

Si c'est le repository de quelqu'un d'autre :
1. **Fork** le repository d'abord
2. Push vers votre fork
3. Créez une **Pull Request** vers l'original

---

## 🎯 Recommandation

**Utilisez GitHub Desktop** - C'est le plus simple et le plus visuel ! 😊

1. Ouvrez GitHub Desktop
2. Add Local Repository → `outer-juno`
3. Cochez les fichiers
4. Commit
5. Push

**C'est fait en 2 minutes !** ✨
