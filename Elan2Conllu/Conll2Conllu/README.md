# Explications Katharine
Ce dossier contient les scripts de conversion des fichiers Conll issus d'ELAN (voir `Elan2Conll`) vers le format Conllu.

Ils s'appuient sur des fichiers csv de correspondance qui se trouvent dans les dossiers langue à la racine d'Autogramm (ex : `Autogramm > Zaar > tables_conversion.csv`)

Le script est lancé avec la commande `python3 Conll2Conllu.py` avec l'environnement suivant :

![image](https://user-images.githubusercontent.com/98810400/171854381-d46e3db6-69d8-41d4-8642-9c2081c39b48.png)

NB : Les noms du dossier à traiter et des tables sont attribués par défaut avec les noms spécifiques présents sur l'image. (Modifiable dans le script aux lignes 42 à 45)


Après exécution du script, un dossier resultat_conversion_conllu sera créé contenant les conllu convertis :

![image](https://user-images.githubusercontent.com/98810400/171854322-823dbd78-251f-4681-bbf9-c5bf792604ed.png)


Remarques importantes : 
1) Un lemme manquant sera rempli dans le conllu final par sa forme.
2) En cas de conflit, ce sera le pos de la table GE qui sera conservé au détriment de celui de la table RX.
