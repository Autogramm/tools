# --------------------------------------------------------------------------
# Importation des bibliothèques nécessaires
import re
import os
# --------------------------------------------------------------------------
# Fonction permettant de mettre une table de conversion dans un dictionnaire
def makeOneDict(table):
    obj_table = open(table)
    dic = {}
    for l in obj_table :
        column  = l.split(";")
        dic[column[0].rstrip('\n')] = [column[1].rstrip('\n'), column[2].rstrip('\n'), column[3].rstrip('\n')]
    return dic
  
# RQ : pour GE et RX on a :
# pos = dic[cle][0] 
# feats = dic[cle][1]
# gloss = dic[cle][2]
# la "cle" étant donc un élément de la colonne "Split GE" ou "Split RX"
# --------------------------------------------------------------------------
# Fonction pour énoncer les fichiers à traiter (par défaut)
def bonsFichiers():
    reponse = input("Est-ce que les fichiers à traiter sont bien SAY_BC_23mars, et les tables split_GE.csv, split_RX.csv, ponctuation.csv \n(y) pour oui (n) pour non \n")
    if reponse == "y" :
        return True
    else :
        return False 
        
# Fonction si fichiers à traiter sont différents 
def fichiersAmettre():
    dossierConll = input("Dossier conll à traiter : ")
    fichiertableGE = input("Fichier table GE : ")
    fichiertableRX = input("Fichier table RX : ")
    fichiertablePonctuation = input("Fichier table ponctuation : ")
    return dossierConll, fichiertableGE, fichiertableRX, fichiertablePonctuation
# --------------------------------------------------------------------------
# Fonction principale de la conversion
def conversion():
    # on crée nos dictionnaires
    # on peut ici changer les chemins et/ou les fichiers à traiter si besoin
    if bonsFichiers():
        dossierConll = "./SAY_BC_23mars"
        table_GE = "./split_GE.csv"
        table_RX = "./split_RX.csv"
        table_PUNCT = "./ponctuation.csv"
        dict_GE, dict_RX, dict_PUNCT = makeOneDict(table_GE), makeOneDict(table_RX), makeOneDict(table_PUNCT)    
    else:
    # sinon on peut renseigner d'autres arguments si ceux par défaut sont incorrects
        try:
            dossierConll, table_GE, table_RX, table_PUNCT = fichiersAmettre()
            dict_GE, dict_RX, dict_PUNCT = makeOneDict(table_GE), makeOneDict(table_RX), makeOneDict(table_PUNCT)           
        except:
            print("fichiers non trouvés")
            
    # on crée un répertoire de résultat, s'il existe déjà alors on continue        
    try:
        os.makedirs("./resultat_conversion_conllu/")
    except:
        pass
        
    files = os.listdir(dossierConll)
    
    for fichierConll in files:
        print(f"fichier en cours de traitement : {fichierConll}")
        with open("./"+dossierConll+"/"+fichierConll, "r", encoding="utf-8") as inputConllu, open("./resultat_conversion_conllu/"+"conversion"+fichierConll+"u", "w", encoding="utf-8") as outputConlluUD:
            # iteration des lignes du fichier conllu en evitant les métadonnées ou les lignes vides
            for l in inputConllu.readlines():
                estPunct = False
                # on ne veut pas traiter les sauts de lignes
                if len(l) == 1:
                        pass
                # on ne traite que les lignes qui ne sont pas des métadonnées
                elif l.startswith('#') == False:
                    inputSplit = l.split('\t')
                    form = str(inputSplit[1]) 
                    lemma = str(inputSplit[2])
                    # on remplit la colonne des lemmes manquants par la forme trouvée (lemme à corriger sur arborator plus tard manuellement)
                    if lemma == "" :
                        inputSplit[2] = inputSplit[1]           
                    # si le lemme rencontré est une ponctuation
                    for clePUNCT in dict_PUNCT.keys():
                        if form == clePUNCT :
                            # on met le pos dans la bonne colonne selon la table (on aurait pu mettre PUNCT directement ici)
                            inputSplit[3] = dict_PUNCT[clePUNCT][0]
                            # suppression des MGloss de la colonne Feats qui n'étaient là que pour la bonne visualisation
                            # dans arborator (ces informations se retrouvent dans MISC donc l'information n'est pas perdue)
                            inputSplit[5] = "_"
                            # dans la colonne MISC, on met une glose par ce qui est attribué pour la glose dans la table
                            inputSplit[9] = re.sub("GE=", "Gloss="+dict_PUNCT[clePUNCT][2]+"|GE=", inputSplit[9])
                            estPunct = True
                            break
                    # si c'est autre chose qu'une ponctuation, on fait le traitement suivant
                    if estPunct == False:
                        # Attention GE et RX ne sont pas toujours contenus dans la dernière colonne MISC
                        # le try/except permet de ne pas afficher d'erreurs
                        try:
                            # on crée une liste feats car il peut y en avoir plusieurs
                            listeFeats = []
                            # extraction des GE et RX de la colonne MISC 
                            extractionGE = re.search("GE=([^|]+)", inputSplit[9]).group(1)
                            trait = re.split("\.", extractionGE)   
                            extractionRX = re.search("RX=([^|]+)", inputSplit[9]).group(1)
                            pos = re.split("\.", extractionRX)
                        except:
                            pass
                        # on parcourt le dictionnaire RX et pour chaque élément on trouve ses feats associés et on les ajoute dans la liste
                        for cleRX in dict_RX.keys():
                            for elem in pos:
                                # nettoyage de l'élément
                                # attention au saut de ligne qui doit être enlevé (RX est souvent en fin de ligne contrairement à GE)
                                elemClean = elem.lstrip('[').rstrip(']').rstrip(']\n')
                                # si on trouve l'élément dans le dictionnaire RX
                                if cleRX == elemClean:
                                    # on met le bon POS
                                    inputSplit[3] = dict_RX[cleRX][0]
                                    # on découpe les Feats s'il y en a plusieurs et on l'ajoute à la liste
                                    if dict_RX[cleRX][1] != "":
                                        elementFeat = dict_RX[cleRX][1].split('|')
                                        listeFeats += elementFeat
                        # si rien n'a été trouvé, on met le underscore par défaut
                        if inputSplit[3] == "":
                            inputSplit[3] = "_"
                            
                        # même chose pour GE
                        for cleGE in dict_GE.keys():
                            for elem in trait:
                                # nettoyage de l'élément
                                elemClean = elem.lstrip('[').rstrip(']')
                                # si on trouve l'élément dans le dictionnaire GE
                                if cleGE == elemClean:
                                    # le pos de RX peut être écrasé par celui de GE s'il y en a un
                                    # -> GE aura le dernier mot sur RX concernant le POS
                                    if dict_GE[cleGE][0] != "" :
                                        inputSplit[3] = dict_GE[cleGE][0]
                                    # on découpe les Feats s'il y en a plusieurs et on l'ajoute à la liste
                                    if dict_GE[cleGE][1] != "":
                                        elementFeat = dict_GE[cleGE][1].split('|')
                                        listeFeats += elementFeat
                                    # s'il y a qqch dans la colonne glose, il faut le mettre dans MISC
                                    # s'il y a déjà le trait "Gloss=" alors remplacer ce qu'il y avait
                                    # si pas de "Gloss=" dans MISC, alors le rajouter avec la glose trouvée
                                    if dict_GE[cleGE][2] != "":
                                        if "Gloss" in l:
                                            inputSplit[9] = re.sub("Gloss=[^|]+", "Gloss="+dict_GE[cleGE][2], inputSplit[9])
                                        else:
                                            inputSplit[9] = re.sub("GE=", "Gloss="+dict_GE[cleGE][2]+"|GE=", inputSplit[9])
                        
                        # on concatène les feats avec "|" et on met le résultat obtenu dans la colonne dédiée aux Feats
                        # si on a aucun Feats, on met la valeur par défaut "_"
                        if listeFeats:
                            # on élimine les doublons
                            featsSansDoublon = list(set(listeFeats))
                            L=[]
                            d={}
                            # si on a un trait qui a plusieurs valeurs différentes, 
                            # les mettre sous le même trait, avec les éléments séparés par une virgule  
                            for e in featsSansDoublon:      
                                trait= re.search("(.*)=", e).group(1)
                                valeur= re.search("=(.*)", e).group(1)
                                # si c'est la première fois qu'on rencontre le trait, on met la valeur qui y est associée
                                if trait not in d:
                                    d[trait]=[valeur]
                                # sinon, on ajoute la nouvelle valeur dans le trait déjà rencontré
                                else:
                                    d[trait].append(valeur)
                            # on joint tous les Feats, avec une virgule séparant les valeurs quand il y en a plusieurs
                            # par ordre alphabétique
                            for key, value in d.items():
                                L.append(key+"="+",".join(sorted(value)))                      
                            # on trie la liste pour avoir les traits dans l'ordre alphabétique également
                            listeFinale = sorted(L)
                            inputSplit[5] = "|".join(listeFinale)
                        else:
                            inputSplit[5] = "_"
                try:
                    # réécrire les lignes métadonnées dont les lignes commencent par "#" 
                    # et la toute première ligne du fichier sans aucune modification
                    # les autres lignes commencçant par "# sent_id" doivent être précédés d'un saut de ligne pour bien séparer les phrases
                    if l.startswith('# sent_id =') == True and '001-' in l:
                        outputConlluUD.write(l)
                    elif l.startswith('# sent_id =') == True:
                        outputConlluUD.write('\n')
                        outputConlluUD.write(l)
                    elif l.startswith('#') == True:
                        outputConlluUD.write(l)
                    # pour les lignes contenant les tokens, les joindre par une tabulation 
                    # attention à ignorer les sauts de ligne : il faut bien un elif avec une ligne de longueur différente de 1
                    # pas de else qui pourrait englober d'autres cas (comme le saut de ligne)
                    elif len(l) != 1:
                        outputConlluUD.write('\t'.join(inputSplit))
                except:
                    print("erreur")
# --------------------------------------------------------------------------
# on appelle la fonction
conversion()
# --------------------------------------------------------------------------