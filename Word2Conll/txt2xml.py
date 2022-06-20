from collections import deque
import re, os , glob
from lxml import etree as ET



"""    Exemple de phrase: 

       1. nau=	war		vet		dagasnia	be		da		loko		kumara.
       S1sg	vouloir	dire	comment		Purp	faire	laplap		patate.douce
       « Je vais expliquer comment on fait le laplap de patates douces. »   """


#regex pour repérer les lignes de traduction libre: elles contiennent des guillemets et ne sont pas précédés de chiffres 
lignetexte = re.compile('(^([0-9]*)) *«|(^([0-9]*)) *\"|(^([0-9]*)) *“')
last_lines = deque(maxlen=2)

#chemin du répertoire contenant le corpus
path = './Corpus'

with open("error.txt", "w", encoding="utf-8") as error: 
    for filename in glob.glob(os.path.join(path, '*.txt')):
        #on compte le nombre de fichiers dans le répertoire
        count = re.findall('[0-9]+', filename)[0]
        with open(os.path.join(os.getcwd(), filename), 'r') as f1, open(f"sungwadia_{count}.xml", "wb") as f2:
                #la première ligne de chaque fichier contient le titre
                first_line = f1.readline()
               
                #on supprime les informations supplémentaires du titre
                #exemple: Vevsale min na= kad	 (vevLL, vevRB) Lala Lui, Rincilla Bani.
                if '(' in first_line:
                    first_line = str(first_line.split('(')[0])
                first_line = ' '.join(first_line.split()).strip()
               
                #on construit le fichier XML
                root = ET.Element("interlinear-text")
                item = ET.SubElement(root, "item", type="title").text = first_line
                phrases = ET.SubElement(root, "phrases")
                sent_id = 0
                for line in f1:
                    #si on trouve une traduction libre
                    if re.search(lignetexte, line):
                        sent_id += 1
                        #on récupère les tokens sur l'avant-dernière ligne
                        form = last_lines[0].split()
                        #on sépare les tokens en morphèmes
                        form_morph = last_lines[0].replace('-',' -').replace('=','= ').split()
                        #on enlève l'identifiant de la phrase au début de la ligne
                        form.pop(0)
                        form_morph.pop(0)
                        #on récupère la glose sur la dernière ligne
                        gloss = last_lines[1].split()
                        #on sépare la glose en morphèmes
                        gloss_morph = last_lines[1].replace('-',' -').split()
                        #on vérifie s'il y a le même nombre de morphèmes sur les lignes 1 et 2
                        if len(form) == len(gloss) and len(form_morph) == len(gloss_morph):
                            index = 1
                            #on efface les guillemets de la traduction libre
                            translation = re.sub("«|»|\"", "", line)
                            #et on efface les espaces et sauts de ligne
                            translation = translation.rstrip()
                            phrase = ET.SubElement(phrases, "phrase")
                            id_sent = ET.SubElement(phrase, "item", num=str(sent_id))
                            trans = ET.SubElement(phrase, "item", type="ft").text = translation
                            words = ET.SubElement(phrase, "words")
                            verif = True  
                            #on concatène les clitiques (la plupart du temps séparés dans le corpus)
                            #exemple : le=	uma au lieu de le=uma
                            new_form = []
                            new_gloss = []
                            i = 0
                            while i < len(form):
                                #cas 1 : Mo=	nau=	mo=	ta=	vet
                                if i < len(form)-4 and form[i].endswith("=") and form[i+1].endswith("=") and form[i+2].endswith("=") and form[i+3].endswith("="):
                                    new_form.append(["@".join(form[i:i+5])][0])
                                    new_gloss.append(["=@".join(gloss[i:i+5])][0])
                                    if i > len(form)-5:
                                        i += 4
                                    else:
                                        i += 5    

                                #cas 2 : I=	ti=	wa=	lua
                                elif i < len(form)-3 and form[i].endswith("=") and form[i+1].endswith("=") and form[i+2].endswith("="):
                                    new_form.append(["@".join(form[i:i+4])][0])
                                    new_gloss.append(["=@".join(gloss[i:i+4])][0])
                                    if i > len(form)-4:
                                        i += 3
                                    else:
                                        i += 4   
                                # cas 3: kami=	ge=	mumlmule
                                elif i < len(form)-2 and form[i].endswith("=") and form[i+1].endswith("="):
                                    new_form.append(["@".join(form[i:i+3])][0])
                                    new_gloss.append(["=@".join(gloss[i:i+3])][0])
                                    if i > len(form)-3:
                                        i += 2
                                    else:
                                        i += 3
                                #cas 4: ti=	baso   
                                elif i < len(form)-1 and form[i].endswith("="):
                                    new_form.append(["@".join(form[i:i+2])][0])
                                    new_gloss.append(["=@".join(gloss[i:i+2])][0])
                                    if i > len(form)-2:
                                        i += 1
                                    else:
                                        i += 2
                                # case 5:        
                                elif i < len(form)-2 and form[i+1].startswith("=") and form[i+2].startswith("="):
                                    new_form.append(["@".join(form[i:i+3])][0])
                                    new_gloss.append(["@=".join(gloss[i:i+3])][0])
                                    if i > len(form)-3:
                                        i += 2
                                    else:
                                        i += 3
                                    
                                # case 6: Irana	=gatgatou 
                                elif i < len(form)-1 and form[i+1].startswith("="):
                                    new_form.append(["@".join(form[i:i+2])][0])
                                    new_gloss.append(["@=".join(gloss[i:i+2])][0])   
                                    if i > len(form)-2:
                                        i += 1
                                    else:
                                        i += 2                
                                else : 
                                    new_form.append(form[i])
                                    new_gloss.append(gloss[i])
                                    i += 1
                                    
                            # on vérifie qu'il y a le même nombre de morphèmes dans chaque token et dans sa glose           
                            for i in range(len(new_form)):    
                                if '-' in new_form[i] or '=' in new_form[i]: 
                                    morph = new_form[i].replace('-',' -').replace('@',' ').split()
                                    glose = new_gloss[i].replace('-',' -').replace('@',' ').split()
                                    if len(morph) == len(glose):
                                        verif = True    
                                    else:
                                        verif = False
                             
                            if verif is True:
                                morph_id = 1
                                #on ajoute chaque token au fichier XML (en les  séparant en morphèmes si besoin)
                                for i in range(len(new_form)):
                                    if '-' in new_form[i] or '=' in new_form[i]: 
                                        morph = new_form[i].replace('-',' -').replace('@',' ').split()
                                        glose = new_gloss[i].replace('-',' -').replace('@',' ').split()
                                        word = ET.SubElement(words, "word")
                                        morphemes = ET.SubElement(word, "morphemes")
                                        for m in range (len(morph)):
                                            #si une phrase se termine par un clitique, on ajoute la phrase au fichier d'erreur
                                            if morph[len(morph)-1] == '=':
                                                error.write(f"Erreur dans la partie {first_line}, phrase {str(sent_id)}: la phrase se termine par un clitique. \n{new_form}\n{new_gloss}\n\n")
                                            else:
                                                morph_ele = ET.SubElement(morphemes, "morph")
                                                str_id = str(morph_id)
                                                id_m = ET.SubElement(morph_ele, "item", num=str_id)
                                                morph_txt = ET.SubElement(morph_ele, "item", type="txt").text = morph[m].strip(',|.|:|»|«|"|;')
                                                morph_gls = ET.SubElement(morph_ele, "item", type="gls").text = glose[m].strip(',|.|:|»|«|"|;')
                                                morph_id += 1

                                    else:
                                        word = ET.SubElement(words, "word")
                                        morphemes = ET.SubElement(word, "morphemes")
                                        morph_ele = ET.SubElement(morphemes, "morph")
                                        str_id = str(morph_id)
                                        id_w = ET.SubElement(morph_ele, "item", num=str_id)
                                        morph_txt = ET.SubElement(morph_ele, "item", type="txt").text = new_form[i].strip(',|.|:|»|«|"')
                                        morph_gls = ET.SubElement(morph_ele, "item", type="gls").text = new_gloss[i].strip(',|.|:|»|«|"')
                                        morph_id += 1
                            else: 
                                #si un mot n'a pas le même nombre de morphèmes dans sa glose que dans sa forme, on écrit la phrase dans le fichier d'erreur
                                error.write(f"{first_line} : Erreur dans la phrase {str(sent_id)}: un des mots n'a pas le même nombre de morphèmes dans sa forme et sa glose. \n")
                        else:
                            error.write(f"{first_line}: Erreur dans la phrase {str(sent_id)}: \n forme ({str(len(form))}){str(form)} \n glose ({str(len(gloss))}) {str(gloss)} \n form morph ({str(len(form_morph))}) {str(form_morph)} \n gloss morph ({str(len(gloss_morph))}) {str(gloss_morph)} \n\n")                         
                    last_lines.append(line)
                tree = ET.ElementTree(root)
                tree.write(f2, pretty_print=True, xml_declaration=True,   encoding="utf-8")