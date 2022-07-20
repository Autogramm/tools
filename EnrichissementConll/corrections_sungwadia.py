import conll, re, sys, os
from pathlib import Path
import spacy

nlp=spacy.load("fr_core_news_md")

def folder2ConllTrees(folder):
    """
    input : a folder of conll files
    output : a dictionnary, the keys will be the files names', and the value for each key is a list of conll Trees
    """
    conlldict={}
    files_l=os.listdir(folder)
    for file in files_l:
        path = Path(f"{folder}/{file}")
        if path.is_file():
            conll_Tree=conll.conllFile2trees(path)
            conlldict[file]=conll_Tree
    return conlldict

def makeRegExFromDictKeys(dict):
    """
    input : a dictionnary, the keys must be the different affixes the regex should look for
    output : a compiled RegEx of every affix like so (affix1$|affix2$...)
    The use of a dictionnary isn't absolutely necessary for this process, but it allows to use
    the same dictionnary in the function responsible for adding the Gloss based on these suffixes
    making it so that you only need to modify one variable if needed.
    """
    string=""
    for key in dict.keys():
        if string:
            string=f"{string}|{key}$"
        else:
            string=f"{key}$"
    
    string=f"({string})"
    return re.compile(string)

def tokenType(conll_Tree,i,sent,id):
    """
    input : a conll_Tree Object, the index of a sentence in this tree, the id of a token
    output : will add the feature "TokenType=Aff" if there's a "-" in the text
        or "TokenType=Clit" if there's a "="
    """
    if re.search(r"\-",sent[id]['t']):
        conll_Tree[i][id]["TokenType"]="Aff"
    elif re.search(r"=",sent[id]['t']):
        conll_Tree[i][id]["TokenType"]="Clit"    
    return True

def nomPropresMaj(conll_Tree,i,sent,id):
    """
    input : a conll_Tree Object, the index of a sentence in this tree, the id of a token
    output : will make it so every capitalized lemma has the MISC Feature "Gloss=NP"
    """
    if re.match(r"[A-Z][a-z]+$",sent[id]['lemma']) and sent[id]['Gloss']!="NP":
        if sent[id]['Gloss']!=sent[id]['lemma']:
            conll_Tree[i][id]['lemma']=conll_Tree[i][id]['lemma'].lower()
        else:
            conll_Tree[i][id]['Gloss']="NP"
        return True

def aorPersonNumber(conll_Tree,i,sent,id):
    """
    input : a conll_Tree Object, the index of a sentence in this tree, the id of a token
    output : will give Aspect|Number|Person|Clusivity|tag features to token matching the RegEx below
    
    """
    if re.match("Aor(1|2|3)(sg|pl)(incl)?",sent[id]['Gloss']):
        m=re.match("Aor(1|2|3)(sg|pl)(incl)?",sent[id]['Gloss'])
        person=m.group(1)
        number=m.group(2)
        clusivity=m.group(3)
        conll_Tree[i][id]["Aspect"]="Aor"
        conll_Tree[i][id]["Person"]=person
        if number=="sg":
            conll_Tree[i][id]["Number"]="Sing"
        elif number=="pl":
            conll_Tree[i][id]["Number"]="Plur"

        if clusivity:
            conll_Tree[i][id]['Clusivity']=clusivity.capitalize()
    elif re.match("Aor(Sg|Pl|sg|pl)",sent[id]['Gloss']):
        m=re.match("Aor(Sg|Pl|sg|pl)",sent[id]['Gloss'])
        number=m.group(1)
        conll_Tree[i][id]["Aspect"]="Aor"
        if number=="sg" or number=="Sg":
            conll_Tree[i][id]["Number"]="Sing"
        elif number=="pl" or number=="Pl":
            conll_Tree[i][id]["Number"]="Plur"
    conll_Tree[i][id]['tag']='AUX'
    return True

def featuresPronoms(conll_Tree,i,sent,id,pronGloss):
    """
    input : a conll_Tree Object, the index of a sentence in this tree, the id of a token
    output : will give Case|deprel|Number|Person|Clusivity|ta|TokenType|PronType features to token matching the RegEx below
    """
    if re.match(pronGloss,sent[id]['Gloss']):
        m=re.search(pronGloss,sent[id]['Gloss'])
        pronType=m.group(1)
        person=m.group(2)
        number=m.group(3)
        clusivity=m.group(4)
        conll_Tree[i][id]['Person']=person

        if pronType=="O":
            conll_Tree[i][id]['deprel']="comp:obj"
            conll_Tree[i][id]['Case']="Acc"

        elif pronType=="P":
            conll_Tree[i][id]['deprel']="mod:poss"
            conll_Tree[i][id]['Case']="Poss"

        elif pronType=="S":
            conll_Tree[i][id]['deprel']="subj"
            conll_Tree[i][id]['Case']="Nom"

        elif pronType=="Obl":
            conll_Tree[i][id]['deprel']="comp:obl"  

        elif pronType=="I":
            conll_Tree[i][id]['deprel']="dislocated"

        if number == 'sg' :

            conll_Tree[i][id]['Number']="Sing"

        elif number == 'pl' :

            conll_Tree[i][id]['Number']="Plur"
        
        elif number == 'du' :

            conll_Tree[i][id]['Number']="Dual"

        if clusivity:
            conll_Tree[i][id]['Clusivity']=clusivity.capitalize()

        

        conll_Tree[i][id]['tag']='PRON'

        conll_Tree[i][id]['PronType']="Pers"

        conll_Tree[i][id]['TokenType']="Clit"

        
    return True

def createCorrespondanceDictFromFile(file):
    """
    input : a csv file having three columns "fréquence, Gloss, UD" the Gloss column containing 
        a possible gloss for a token, the fréquence column showing the number of times it is used and
        the UD columns giving a UD correspondance of what can be understood from the Gloss
    output : a dictionnary having the content of the Gloss column as keys and the content of the UD column
        as values
    """
    correspondanceDict={}
    regList=re.compile(r".+?\t(.+?)\t([^\n\t]+)")
    with open(file,"r",encoding="UTF-8") as f:
        f.readline()
        line=f.readline()
        while line:
            if re.match(regList,line):
                m=re.match(regList,line)
                list_feat_value=[(x.split("=")[0],x.split("=")[1]) for x in m.group(2).split("|")]
                correspondanceDict[m.group(1)]=list_feat_value
            line=f.readline()
    return correspondanceDict

def addFromCorrespondanceFile(conll_Tree,i,sent,id,corresDict):
    """
    input : a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token and 
        a dictionnary created using createCorrespondanceDictFromFile
    output : will add the UD correspondances from the dictionnary to the conll_Tree
    """
    glosses=sent[id]['Gloss'].split(".")
    for gloss in glosses:
        if corresDict.get(gloss,False):
            for feat,value in corresDict[gloss]:
                if conll_Tree[i][id].get(feat,"_")=="_":
                    conll_Tree[i][id][feat]=value
    return True

def reduplication(conll_Tree,i,sent,id):
    """
    input : a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token
    output : If the Gloss contains "Red", will add the feature Reduplicated=Yes, the effect of the reduplication in the Gloss feature
        a MGloss showing the reduplication on a motphosyntactic level and a feature MSeg showing the reduplication on a morphological level
    """
    if re.match(r"Red",sent[id]['Gloss']):
        m=re.match(r"(Red)(.*?)\.(.*)",sent[id]['Gloss'])
        act=m.group(2)
        gloss=m.group(3)
        conll_Tree[i][id]['Reduplicated']="Yes"
        conll_Tree[i][id]['Gloss']=m.group(3)
        if act:
            conll_Tree[i][id]['MGloss']=f'{act}~{gloss}'
        else:
            conll_Tree[i][id]['MGloss']=f'RED~{gloss}'

        cv=re.match(r"(..)(..)",sent[id]['lemma'])
        cvc=re.match(r"(...)(...)",sent[id]['lemma'])

        if cvc and cvc.group(1)==cvc.group(2):
            lemma=sent[id]['lemma']
            conll_Tree[i][id]['MSeg']=f'{cvc.group(1)}~{lemma[3:]}'
        elif cv and cv.group(1)==cv.group(2):
            lemma=sent[id]['lemma']
            conll_Tree[i][id]['MSeg']=f'{cv.group(1)}~{lemma[2:]}'
        else:
            #Pour les cas où la voyelle est changée en "i" dans la reduplication
            lemma=sent[id]['lemma']
            red_dif=re.match(r"(.+?i)",sent[id]['lemma'])
            if red_dif :
                conll_Tree[i][id]['MSeg']=f'{red_dif.group(1)}~{lemma[2:]}'

def prefixesGloss(pRegEx,prefixes,conll_Tree,sent,i,id):
    """
    input :a compiled Regex made using makeRegExFromDictKeys, the dictionnary used to build the RegEx,
      a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token
    output : will add a MGloss and MSeg feature showing how to decompose the token and add the tag "VERB"
    """
    if re.match(pRegEx,sent[id]['t']):
        m=re.match(pRegEx,sent[id]['t'])
        conll_Tree[i][id+1]['t']=f"{sent[id]['t']}{sent[id+1]['t']}"
        conll_Tree[i][id+1]['MGloss']=f"{prefixes[m.group(1)]}-{sent[id+1]['t']}"
        conll_Tree[i][id+1]['MSeg']=f"{sent[id]['t']}{sent[id+1]['t']}"
        conll_Tree[i][id+1]['tag']="VERB"

def suffixesGloss(sRegEx,suffixes, conll_Tree,sent,i,id):
    """
    input :a compiled Regex made using makeRegExFromDictKeys, the dictionnary used to build the RegEx,
      a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token
    output : will add a MGloss and MSeg feature showing how to decompose the token and add the tag "VERB"
    """
    if re.match(sRegEx,sent[id]['t']):
        m=re.match(sRegEx,sent[id]['t'])
        conll_Tree[i][id-1]['t']=f"{sent[id-1]['t']}{sent[id]['t']}"
        conll_Tree[i][id-1]['MGloss']=f"{sent[id-1]['t']}-{suffixes[m.group(1)]}"
        conll_Tree[i][id-1]['MSeg']=f"{sent[id-1]['t']}{sent[id]['t']}"
        conll_Tree[i][id-1]['tag']="VERB"  

def ifEqualOrDashInTextEqualInGloss(conll_Tree,sent,i,id):
    """
    input : a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token
    output : if there is a "=" or a "-" in the text, it is added to the Gloss
    """
    #If the equal or dash is in the Gloss but not in the text
    if re.match(r"(\-|=).+",sent[id]['Gloss']) and not re.match(r"(\-|=).+",sent[id]['t']):
        m=re.match(r"(\-|=).+",sent[id]['Gloss'])
        eq=m.group(1)
        conll_Tree[i][id]['t']=f"{eq}{conll_Tree[i][id]['t']}"
    elif re.match(r".+(\-|=)",sent[id]['Gloss']) and not re.match(r".+(\-|=)",sent[id]['t']):
        m=re.match(r".+(\-|=)",sent[id]['Gloss'])
        eq=m.group(1)
        conll_Tree[i][id]['t']=f"{conll_Tree[i][id]['t']}{eq}"

    #If the equal or dash is in the text but not in the gloss
    if re.match(r"(\-|=).+",sent[id]['t']) and not re.match(r"(\-|=).+",sent[id]['Gloss']):
        m=re.match(r"(\-|=).+",sent[id]['t'])
        eq=m.group(1)
        conll_Tree[i][id]['Gloss']=f"{eq}{conll_Tree[i][id]['Gloss']}"
    elif re.match(r".+(\-|=)",sent[id]['t']) and not re.match(r".+(\-|=)",sent[id]['Gloss']):
        m=re.match(r".+(\-|=)",sent[id]['t'])
        eq=m.group(1)
        conll_Tree[i][id]['Gloss']=f"{conll_Tree[i][id]['Gloss']}{eq}"

def pleaseSpacyGiveMeSomeTags(conll_Tree,sent,i,id,nlp):
    """
    Input : a conll_Tree, the index of a sentence, a sentence Tree from the conll_Tree, the id of a token, 
        a nlp parsing function made using spacy
    Output : adds tags to a conll based on the tags the parser would give to the gloss
    """
    if sent[id]['tag']=="_" and re.match(r"[a-z]+$",sent[id]['Gloss']):
        token=nlp(sent[id]['Gloss'].strip("-"))
        for tok in token:
            if tok.pos_!='ADJ' or re.match(r"(masu?|toli|mawuti?|lebata|tuara?|n wae|valu)",sent[id]['lemma']):
                conll_Tree[i][id]['tag']=tok.pos_
            else:
                conll_Tree[i][id]['tag']="VERB|ATTRIBUTIF"

def splitAmalagameInTwo(amalgames,aRegEx,conll_Tree):
    """
    Careful using this function, the original amalgamate is added in the feature "Amal" but isn't seen in the text before post processing
    Input : a dict of amalgamate having the amalgamates as keys, a compiled RegEx made using makeRegexFromDictKeys, a conll_Tree Object
    Output : separates the amalgamates in two eg: in french "du" becomes "de le". 
        Using this function the tag CCONJ is given to the first new token and the original Gloss is given to the second one
    """
    for i, sent in enumerate(conll_Tree):
        
        sent_tmp=conll.Tree()
        sent_tmp.sentencefeatures=conll_Tree[i].sentencefeatures
        amal_c=1

        for id in sent:

            # Désamalgames
            if re.match(aRegEx,sent[id]['t']):
                # sent_tmp[f'{amal_c}-{amal_c+1}']={'t': sent[id]['t']}
                # for key in sent[id].keys():
                #     if key!='t':
                #         sent_tmp[f'{amal_c}-{amal_c+1}'][key]='_'

                m=re.match(aRegEx,sent[id]['t'])
                amal=m.group(1)
                desamal=amalgames[amal]
                sent_tmp[amal_c]={'t' : desamal[0], 'lemma' : desamal[0], 'tag' : 'CCONJ', 'Amal' : amal}
                for key in sent[id].keys():
                    if key!='t' and key!='tag' and key!='lemma'and key!='Gloss':
                        sent_tmp[amal_c][key]=sent[id][key]
                sent_tmp[amal_c+1]={'t' : desamal[1],'lemma' : desamal[1], 'Gloss' : sent[id]['Gloss']}
                for key in sent[id].keys():
                    if key!='t' and key!='Gloss' and key!='lemma':
                        sent_tmp[amal_c+1][key]=sent[id][key]
                amal_c+=2

            else:
                sent_tmp[amal_c]=sent[id]
                amal_c+=1
        
        conll_Tree[i]=sent_tmp

def correction_conllTree(conll_Tree,correspondanceDict):
    """
    Input : a conll_Tree object, a correspondanceDict made using createCorrespondanceDictFromFile
    Output : a number of corrections and additions to the conll_Tree 
    """
    ### Données à initialiser pour les différentes corrections
    pronGloss=re.compile(r'.*(S|P|O|Obl|I)([123])(pl|sg|du)(in|ex)?.*')
    prefixes={"va-" : "CAUS", "vaga-" : "RECIP", "vagal-" : "RECIP"}
    suffixes={"-si" : "TR", "-gi" : "TR", "-agi" : "TR"}
    
    pRegEx=makeRegExFromDictKeys(prefixes)
    sRegEx=makeRegExFromDictKeys(suffixes)
    

    for i, sent in enumerate(conll_Tree):
        


        for id in sent.keys():
            conll_Tree[i][id]['gov']

            nomPropresMaj(conll_Tree,i,sent,id)

            featuresPronoms(conll_Tree,i,sent,id,pronGloss)

            reduplication(conll_Tree,i,sent,id)
            
            prefixesGloss(pRegEx,prefixes,conll_Tree,sent,i,id)

            suffixesGloss(sRegEx,suffixes, conll_Tree,sent,i,id)
                   
            #Clitiques Possessifs
            # if re.match(r"P\d",sent[id]['Gloss']) and re.match(r".+-$",sent[id]['t']):

            addFromCorrespondanceFile(conll_Tree,i,sent,id,correspondanceDict)

            ifEqualOrDashInTextEqualInGloss(conll_Tree,sent,i,id)

            tokenType(conll_Tree,i,sent,id)

            aorPersonNumber(conll_Tree,i,sent,id)

            pleaseSpacyGiveMeSomeTags(conll_Tree,sent,i,id,nlp)


    
    amalgames={"kat" : ["ka","ti"],"kae" : ["ka","ge"], "tot" : ["toga","ge"], "ton" : ["toga","ne"]}
    aRegEx=makeRegExFromDictKeys(amalgames)
    splitAmalagameInTwo(amalgames,aRegEx,conll_Tree)

    return conll_Tree

def correction_Folder(folder,correspondanceDict):
    """
    input : A folder, a correspondanceDict made using createCorrespondanceDictFromFile
    output : a dictionnary of the modified trees, using the filename as key
    """
    conlldict=folder2ConllTrees(folder)
    correctedTrees={}

    for file in conlldict.keys():
        correctedTree=correction_conllTree(conlldict[file],correspondanceDict)
        correctedTrees[file]=(correctedTree)

    return correctedTrees

def rewriteCorrectedFiles(correctedTrees,outputFolder="corrected/"):
    """
    input : A dictionnary created using correction_Folder, an output folder
    outut : the rewriting of the corrected trees in the new folder
    """
    path=Path(outputFolder)
    if not path.is_dir():
        os.makedirs(outputFolder)
    for file in correctedTrees.keys():
        conll.trees2conllFile(correctedTrees[file], f"{outputFolder}/{file}")
    return True

def fromConllFolder2CorrectedConllFolder(folder,correspondanceDict,output="corrected/"):
    """
    input : a folder of conll files, a correspondanceDict made using createCorrespondanceDictFromFile and an output folder
    output : A new folder containing modified conll files, these will need post processing using another script
    """
    correctedTrees=correction_Folder(folder,correspondanceDict)
    rewriteCorrectedFiles(correctedTrees, output)
    return True

if __name__ == "__main__":
    folder=sys.argv[1]
    correspondanceFile=sys.argv[2]
    correspondanceDict=createCorrespondanceDictFromFile(correspondanceFile)
    fromConllFolder2CorrectedConllFolder(folder,correspondanceDict)