from collections import deque
import re, os , glob
from lxml import etree as ET

#lines ending with quotation marks contain the free translation
lignetexte = re.compile("»$|\"$")
last_lines = deque(maxlen=2)

path = './CorpusPart'

with open("error_test.txt", "w", encoding="utf-8") as error: 
    for filename in glob.glob(os.path.join(path, '*.txt')):
        #counting the number of parts in the corpus
        count = re.findall('[0-9]+', filename)[0]
        with open(os.path.join(os.getcwd(), filename), 'r') as f1, open(f"sungwadia_test{count}.xml", "wb") as f2:
                #the first line of each file contains the title
                first_line = f1.readline()
                if '(' in first_line:
                    first_line = first_line.split('(')[0]
                first_line = first_line.strip()
                #building the XML file
                root = ET.Element("interlinear-text")
                item = ET.SubElement(root, "item", type="title").text = first_line
                phrases = ET.SubElement(root, "phrases")
                error.write(first_line + '\n\n')
                sent_id = 0
                for line in f1:
                    #if the line contains quotation marks, it is the free translation
                    if re.search(lignetexte, line):
                        if 'NO GLOSSING' not in last_lines[1] and 'NO TRANSLATION' not in last_lines[0]:
                            sent_id += 1
                            #getting the tokens on the first line of the interlinear gloss
                            form = last_lines[0].split()
                            #separating tokens into morphemes
                            form_morph = last_lines[0].replace('-',' -').split()
                            #deleting the sentence id at the beginning of the line
                            form.pop(0)
                            form_morph.pop(0)
                            #the second line of the interlinear gloss contains the gloss
                            gloss = last_lines[1].split()
                            #separating gloss into morphemes
                            gloss_morph = last_lines[1].replace('-',' -').split()
                            #checking if there is the same number of tokens and morphemes on line 1 and 2
                            if len(form) == len(gloss) and len(form_morph) == len(gloss_morph):
                                index = 1
                                #deleting quotations marks from the translation
                                translation = re.sub("«|»|\"", "", line)
                                #deleting spaces and newlines from the translation
                                translation = translation.rstrip()
                                phrase = ET.SubElement(phrases, "phrase")
                                id_sent = ET.SubElement(phrase, "item", num=str(sent_id))
                                trans = ET.SubElement(phrase, "item", type="ft").text = translation
                                words = ET.SubElement(phrase, "words")
                                verif = True  
                                #concatenating clitics (they were separated in the corpus)
                                new_form = []
                                new_gloss = []
                                i = 0
                                while i < len(form):
                                    #case 1 : 
                                    if i < len(form)-4 and form[i].endswith("=") and form[i+1].endswith("=") and form[i+2].endswith("=") and form[i+3].endswith("="):
                                        new_form.append(["".join(form[i:i+5])][0])
                                        new_gloss.append(["=".join(gloss[i:i+5])][0])
                                        if i > len(form)-5:
                                            i += 4
                                        else:
                                            i += 5    
                                    # case 2: 
                                    if i < len(form)-4 and form[i].endswith("=") and form[i+1].endswith("=") and form[i+2].endswith("=") and form[i+3].endswith("="):
                                        new_form.append(["".join(form[i:i+5])][0])
                                        new_gloss.append(["=".join(gloss[i:i+5])][0])
                                        if i > len(form)-5:
                                            i += 4
                                        else:
                                            i += 5                               
                                    #case 3 : 
                                    elif i < len(form)-3 and form[i].endswith("=") and form[i+1].endswith("=") and form[i+2].endswith("="):
                                        new_form.append(["".join(form[i:i+4])][0])
                                        new_gloss.append(["=".join(gloss[i:i+4])][0])
                                        if i > len(form)-4:
                                            i += 3
                                        else:
                                            i += 4                                
                                    # case 4: 
                                    elif i < len(form)-2 and form[i].endswith("=") and form[i+1].endswith("="):
                                        new_form.append(["".join(form[i:i+3])][0])
                                        new_gloss.append(["=".join(gloss[i:i+3])][0])
                                        if i > len(form)-3:
                                            i += 2
                                        else:
                                            i += 3
                                    #case 5:     
                                    elif i < len(form)-1 and form[i].endswith("="):
                                        new_form.append(["".join(form[i:i+2])][0])
                                        new_gloss.append(["=".join(gloss[i:i+2])][0])
                                        if i > len(form)-2:
                                            i += 1
                                        else:
                                            i += 2
                                    # case 6:             
                                    elif i < len(form)-2 and form[i+1].startswith("=") and form[i+2].startswith("="):
                                        new_form.append(["".join(form[i:i+3])][0])
                                        new_gloss.append(["=".join(gloss[i:i+3])][0])
                                        if i > len(form)-3:
                                            i += 2
                                        else:
                                            i += 3
                                    # case 7:     
                                    elif i < len(form)-1 and form[i+1].startswith("="):
                                        new_form.append(["".join(form[i:i+2])][0])
                                        new_gloss.append(["=".join(gloss[i:i+2])][0])   
                                        if i > len(form)-2:
                                            i += 1
                                        else:
                                            i += 2
                                                        
                                    else : 
                                        new_form.append(form[i])
                                        new_gloss.append(gloss[i])
                                        i += 1
                                        
                                        
                                # checking if there is the same number of morphemes in each token            
                                for i in range(len(new_form)):    
                                    if '-' in new_form[i] or '=' in new_form[i]: 
                                        morph = new_form[i].replace('-',' -').replace('-',' =').split()
                                        glose = new_gloss[i].replace('-',' -').replace('-',' =').split()                                         
                                        if len(morph) == len(glose):
                                            verif = True    
                                        else:
                                            verif = False
                                 
                                if verif is True:
                                    morph_id = 1
                                    #separating each token into morphemes and adding each morpheme to the XML file
                                    for i in range(len(new_form)):
                                        if '-' in new_form[i] or '=' in new_form[i]: 
                                            morph = new_form[i].replace('-',' -').replace('=',' =').split()
                                            glose = new_gloss[i].replace('-',' -').replace('=',' =').split()
                                            word = ET.SubElement(words, "word") 
                                            id_w = ET.SubElement(word, "test")
                                            morphemes = ET.SubElement(word, "morphemes")
                                            for m in range (len(morph)):
                                                if morph[len(morph)-1] == '=':
                                                    error.write(f"Erreur dans la phrase {str(sent_id)}: la phrase se termine par un clitique. \n{new_form}\n{new_gloss}\n\n")
                                                elif len(morph) != len(glose): 
                                                    error.write(f"Erreur dans la phrase {str(sent_id)}: le nombre de morphèmes sur les lignes 1 et 2 n'est pas égal. \n{new_form}\n{new_gloss}\n\n")
                                                else:
                                                    morph_ele = ET.SubElement(morphemes, "morph")
                                                    str_id = str(morph_id)
                                                    id_m = ET.SubElement(morph_ele, "item", num=str_id)
                                                    morph_txt = ET.SubElement(morph_ele, "item", type="txt").text = morph[m].strip(",|.")
                                                    morph_gls = ET.SubElement(morph_ele, "item", type="gls").text = glose[m].strip(",|.")
                                                    morph_id += 1

                                        else:
                                            word = ET.SubElement(words, "word")
                                            morphemes = ET.SubElement(word, "morphemes")
                                            morph_ele = ET.SubElement(morphemes, "morph")
                                            str_id = str(morph_id)
                                            id_w = ET.SubElement(morph_ele, "item", num=str_id)
                                            morph_txt = ET.SubElement(morph_ele, "item", type="txt").text = new_form[i].strip(",|.")
                                            morph_gls = ET.SubElement(morph_ele, "item", type="gls").text = new_gloss[i].strip(",|.")
                                            morph_id += 1
                                else:  
                                    error.write(f"Erreur dans la phrase {str(sent_id)}: le nombre de morphèmes sur les lignes 1 et 2 n'est pas égal. \n{new_form}\n{new_gloss}\n\n")  
                                    index += 1
                            elif len(new_form) != len(new_gloss): 
                                error.write(f"Erreur dans la phrase {str(sent_id)}: le nombre de mots sur les lignes 1 et 2 n'est pas égal. \n{new_form}\n{new_gloss}\n\n") 
                            elif len(form_morph) != len(gloss_morph):
                                error.write(f"Erreur dans la phrase {str(sent_id)}: le nombre de morphèmes sur les lignes 1 et 2 n'est pas égal. \n{new_form}\n{new_gloss}\n\n")               
                    last_lines.append(line)
                tree = ET.ElementTree(root)
                tree.write(f2, pretty_print=True, xml_declaration=True,   encoding="utf-8")