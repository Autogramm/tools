# Explications Salomé
Ce dossier contient les scripts de conversion de texte issu de Word vers Conll. 

La conversion se structure en trois étapes: 
1. Séparation du corpus en parties (script split.py)
2. Conversion des fichiers du corpus au format XML EMELD (script txt2xml.py)
3. Conversion des fichiers XML au format Conll (script xml2conll.py)

### Prérequis
Les trois scripts et le corpus doivent être placés dans un dossier contenant trois sous-dossiers (CoNLL, Corpus et XML) comme ceci: 

![environment](https://user-images.githubusercontent.com/95420208/178999757-5986cb8c-c91b-4ef8-afc3-c00908572dbc.png)

Pour pouvoir manipuler plus facilement le corpus, le texte issu de Word doit être converti ou copié dans un fichier au format txt.

---

### Séparation du corpus
Le script split.py prend en entrée un fichier au format txt (ici "sungwadia.txt", ligne 5). Chaque partie du corpus est séparée par une ligne de tirets et commence par une ligne de titre: 

![example](https://user-images.githubusercontent.com/95420208/179001993-b4c0d237-7acf-4fc0-b855-4973e810712e.png)

Le script produit en sortie un fichier txt par partie. Les fichiers sont enregistrés dans le dossier 'Corpus'. 

---

### Conversion des fichiers txt en XML
Le script txt2xml traite un à un les fichiers du dossier Corpus produits par le script précédent. Cette étape intermédiaire en XML permet de mieux structurer les informations de la glose interlinéraire. Le format retenu est le format EMELD dont la structure est la suivante: 

![xml](https://user-images.githubusercontent.com/95420208/179007399-c28ba5bb-03b9-497b-b3ca-9cd8fb0417ad.png)

Les fichiers XML en sortie sont enregistrés dans le dossier XML. 

---

### Conversion des fichiers XML en Conll
Le script xml2conll prend en entrée les fichiers du dossier XML et les transforme en fichier Conll. Le découpage en morphème effectué à l'étape précédente est conservé. Toutes les informations de la glose sont contenues dans les traits Gloss. 

Les fichiers de sortie sont enregistrés dans le dossier CoNLL. 
