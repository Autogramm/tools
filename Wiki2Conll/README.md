# Wiki2Conll
Ce dossier contient les scripts de conversion du [wiki du breton](https://arbres.iker.cnrs.fr/index.php?title=Arbres:Le_site_de_grammaire_du_breton) vers Conll.

Le script récupère tous les tableaux du type prettytable. Le code source d'un tableau "standard" ressemble à ceci : 

```
{| class="prettytable"
|(3)|| Ar c'hein || '''eûz a''' || '''eul''' || '''léstr''' || a zô || kuzed || enn || dour.
|-
||| [[art|le]] <sup>[[5]]</sup>[[kein|dos]] || [[eus|de]] [[a|à]] || [[art|un]] || [[lestr|vaisseau]] || [[R]] [[zo|est]] || [[kuzhat|caché]] || [[P.e|en]].[[art|le]] || [[dour|eau]]
|-
|||colspan="10" | 'La quille d’un vaisseau est cachée dans l'eau.' 
|-
|||||||||||colspan="10" |Le Gonidec (1838[[Le Gonidec (1838 :186-7)|:186-7)]]
|}
```

Il comporte quatre ligne: la ligne de tokens, la ligne de glose, la traduction et la source. 
A cela peuvent s'ajouter une ligne de transcription phonétique, une ligne d'équivalent standardisé en cas de variation dialectale ou une deuxième ligne de source, par exemple lorsqu'une phrase tirée d'un ouvrage est citée dans un autre. 



Le script produit en sortie des fichiers Conll où les informations issues de la glose sont contenues dans le trait Gloss. Les fichiers Conll sont classés par dialectes : Breton Central, Cornouaillais, Léonard, Standard, Trégorrois et Vannetais. Les Conll des tableaux où le dialecte n'est pas spécifié sont regroupés dans un fichier "Inconnu".

