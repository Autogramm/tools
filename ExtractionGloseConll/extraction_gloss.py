import conll, re, os, sys
from pathlib import Path

def folder2conllfiles(folder):
    """
    Function making a list of conll_Trees object from a folder of conll files
    """
    conllist=[]
    files_l=os.listdir(folder)
    for file in files_l:
        path = Path(f"{folder}/{file}")
        if path.is_file():
            conll_file=conll.conllFile2trees(path)
            conllist.append(conll_file)
    return conllist

def listGloss(conllist,blackListFile=False):
    """
    Gives a list of every entry of the Gloss feature from a list of conllTrees
        using a blacklistfile of already extracted glosses
    """
    glosses={}
    if blackList:
        blackList=createBlackListFromFile(blackListFile)
    for conllTree in conllist:
        for tree in conllTree:
            for sent in tree.keys(): 
                gloss=tree[sent]['Gloss']
                text=tree[sent]['t']
                equal=False
                if re.search("=",text):
                    if text.startswith("="):
                        equal="front"
                    else:
                        equal="back"
                if re.search(r"\.", gloss):
                    for g in gloss.split("."):
                        if re.search(r"[A-Z]",g) and not re.search(r'.*(S|P|O|Obl|I)([123])(pl|sg|du)(in|ex)?.*',g):
                            if blackList:
                                if g not in blackList:
                                    if equal:
                                        if equal=="front":
                                            glosses[f"={g}"]=glosses.get(f"={g}",0)+1
                                        elif equal=="back":
                                            glosses[f"{g}="]=glosses.get(f"{g}=",0)+1
                                    else:
                                        glosses[g]=glosses.get(g,0)+1
                            else:
                                if equal:
                                    if equal=="front":
                                        glosses[f"={g}"]=glosses.get(f"={g}",0)+1
                                    elif equal=="back":
                                        glosses[f"{g}="]=glosses.get(f"{g}=",0)+1
                                else:
                                    glosses[g]=glosses.get(g,0)+1
                elif re.search(r"[A-Z]",gloss) and not re.search(r'.*(S|P|O|Obl|I)([123])(pl|sg|du)(in|ex)?.*',gloss):
                    if blackList:
                        if gloss not in blackList:
                            if equal:
                                if equal=="front":
                                    glosses[f"={gloss}"]=glosses.get(f"={gloss}",0)+1
                                elif equal=="back":
                                    glosses[f"{gloss}="]=glosses.get(f"{gloss}=",0)+1
                            else:        
                                glosses[gloss]=glosses.get(gloss,0)+1
                    else:
                        if equal:
                            if equal=="front":
                                glosses[f"={gloss}"]=glosses.get(f"={gloss}",0)+1
                            elif equal=="back":
                                glosses[f"{gloss}="]=glosses.get(f"{gloss}=",0)+1
                        else:        
                            glosses[gloss]=glosses.get(gloss,0)+1
    return glosses

def glossFile(folder,blackListFile,output="gloses.tsv"):
    """
    Writes a tsv file of the gloss extraction from a folder of conll Files
    """
    conllist=folder2conllfiles(folder)
    glosses=listGloss(conllist,blackListFile)
    with open(output,"w",encoding="UTF-8") as f:
        f.write("fréquence\tGloss\tUD\n")
        for g in sorted(glosses, key=glosses.get, reverse=True):
            f.write(f"{glosses[g]}\t{g}\n")


def createBlackListFromFile(file):
    """
    Creates a blacklist of already extracted glosses from
        a file created using this script
    """
    blackList=[]
    regBlackList=re.compile(r".+?\t(.+?)\t.+\n")
    with open(file,"r",encoding="UTF-8") as f:
        line=f.readline()
        while line:
            if re.match(regBlackList,line):
                m=re.match(regBlackList,line)
                blackList.append(m.group(1))
            line=f.readline()
    return blackList


if __name__ == "__main__":
    folder=sys.argv[1]
    if len(sys.argv)>2:
        blackListFile=sys.argv[2]
    glossFile(folder,blackListFile)
    