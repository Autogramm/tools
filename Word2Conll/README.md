# Explications Salomé
Ce dossier contient les scripts de conversion de texte issu de Word vers Conll. 

La conversion se structure en trois étapes: 
1. Séparation du corpus en parties (script split.py)
2. Conversion des fichiers du corpus au format XML (script txt2xml.py)
3. Conversion des fichiers XML au format Conll (script xml2conll.py)

### Prérequis
Les trois scripts et le corpus doivent être placés dans un dossier contenant trois sous-dossiers (CoNLL, Corpus et XML) comme ceci: 
![environment](https://user-images.githubusercontent.com/95420208/178999757-5986cb8c-c91b-4ef8-afc3-c00908572dbc.png)

Pour pouvoir manipuler plus facilement le corpus, le texte doit être enregistrer au format txt.


### Séparation du corpus
Le script split.py prend en entrée un corpus au format txt (ici "sungwadia.txt", ligne 5). Chaque partie du corpus est séparée par une ligne de tirets et commence par une ligne de titre. Le script produit en sortie un fichier txt par partie. Les fichiers sont enregistrés dans le dossier 'Corpus'. 

### Conversion des fichiers txt en XML


### Conversion des fichiers XML en Conll
