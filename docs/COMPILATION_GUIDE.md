# 🔧 Instructions pour Compiler le PDF

## Problème
MiKTeX est installé mais n'est pas dans votre PATH système.

## Solution Rapide

### Option 1 : Ouvrir un nouveau terminal MiKTeX

1. **Cherchez dans le menu Démarrer** : "MiKTeX Console"
2. Ouvrez **MiKTeX Console**
3. Cliquez sur "Packages" → Vérifiez que tous sont installés
4. Fermez la console
5. **Ouvrez un NOUVEAU PowerShell** (important !)
6. Naviguez vers le dossier :
```powershell
cd c:\Users\axelp\.gemini\antigravity\playground\outer-juno
```
7. Compilez :
```powershell
pdflatex -interaction=nonstopmode rapport_final.tex
pdflatex -interaction=nonstopmode rapport_final.tex
```

### Option 2 : Ajouter MiKTeX au PATH

1. Appuyez sur **Win + R**
2. Tapez `sysdm.cpl` et Enter
3. Onglet "Avancé" → "Variables d'environnement"
4. Dans "Variables système", trouvez "Path" → Modifier
5. Ajoutez ce chemin (adapter selon votre installation) :
   ```
   C:\Users\axelp\AppData\Local\Programs\MiKTeX\miktex\bin\x64
   ```
   OU
   ```
   C:\Program Files\MiKTeX\miktex\bin\x64
   ```
6. Cliquez OK partout
7. **Redémarrez PowerShell**
8. Compilez comme ci-dessus

### Option 3 : Utiliser Overleaf (PLUS SIMPLE)

1. Allez sur https://www.overleaf.com/
2. Créez un compte gratuit
3. New Project → Upload Project
4. **Créez un ZIP** contenant :
   - `rapport_final.tex`
   - Le dossier `report/` (avec tous les PNG)
5. Uploadez
6. Le PDF se compile automatiquement !
7. Téléchargez le PDF

## 📁 Créer le ZIP pour Overleaf

Dans PowerShell :
```powershell
cd c:\Users\axelp\.gemini\antigravity\playground\outer-juno
Compress-Archive -Path rapport_final.tex,report -DestinationPath rapport_tsp.zip -Force
```

Puis uploadez `rapport_tsp.zip` sur Overleaf !

## ✅ Vérification

Si MiKTeX fonctionne, après compilation vous devriez avoir :
- `rapport_final.pdf` (le PDF final !)
- `rapport_final.aux`
- `rapport_final.log`
- `rapport_final.toc`

Le fichier important est **rapport_final.pdf** 🎉

---

**Recommandation** : Utilisez Overleaf, c'est beaucoup plus simple et ça fonctionne à tous les coups !
