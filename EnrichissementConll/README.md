#Enrichissement de conll
Ce dossier contient un exemple d'utilisation du module conll permettant de manipuler des fichiers conll facilement en python.

Il contient 2 scripts python : 
- Un premier utilisé pour de l'enrichissement de conll à partir d'un fichier conll contenant uniquement le trait de Glose
- Un second utilisé pour faire du post-traitement plus ou moins nécessaire selon les enrichissements fait avec le premier

Il nécessite la présence du module conll.py présent dans tools/ModulePythonConll

##script 1 :

Il se lance avec la ligne :

    python corrections_sungwadia.py NOM_DU_DOSSIER_DE_FICHIERS_CONLL_A_ENRICHIR FICHIER_DE_CORRESPONDANCES_GLOSES_VERS_UD

Entrées :

    Un dossier de fichiers conll à enrichir à partir des traits déjà présents
        (un exemple se trouve dans le dossier sous le nom : "python_test/")

    Un dossier de correspondance de traits de Glose vers UD
        (un exemple se trouve dans le dossier : "gloses_propositionsUD_v3.csv")
        (il a été créé à l'aide du script "extraction_gloss.py")

Sorties :

    Un dossier "corrected/" sera créé contenant les conll modifiés

##script 2 :

Il se lance avec la ligne :


    python post_traitement.py NOM_DU_DOSSIER_DE_FICHIERS_CONLL_ENRICHIS


Entrées :

    Un dossier comprenant des fichiers conll enrichis à l'aide du script précédent
        (un exemple se trouve dans le dossier sous le nom : "corrected/")

Sorties :

    Un dossier nommé "post_traitement/" comprenant les fichiers conll post-traités