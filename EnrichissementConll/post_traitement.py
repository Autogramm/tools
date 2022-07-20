import re
import sys
import os
import os.path

def removeMinusOneFromConllFile(lines):
    """
    Function to remove the "-1" in the gov column of conll Files
    """
    i=0
    while i<len(lines):
        if re.search("-1",lines[i]):
            lines[i]=re.sub("-1","_",lines[i])
        i+=1
    return lines

def correctAmal(lines):
    lines_corrected=[]
    i=0
    while i<len(lines)-1:
        if re.search(r"Amal=",lines[i]):
            m=re.search(r"Amal=([^\t\n]+)",lines[i])
            amalgame=m.group(1)
            m=re.match(r"(\d+).*",lines[i])
            id1=m.group(1)
            m=re.match(r"(\d+).*",lines[i+1])
            id2=m.group(1)
            lines_corrected.append(f"{id1}-{id2}\t{amalgame}\t_\t_\t_\t_\t_\t_\t_\t_\n")
            lines_corrected.append(lines[i])
        else:
            lines_corrected.append(lines[i])
        if i==len(lines):
            lines_corrected.append(lines[i+1])
        i+=1
    return lines_corrected

def rewritePostProcessedFile(lines,file):
    with open(f"post_traitement/{file}","w") as f:
        for line in lines:
            f.write(line)
    return True

def removeMinusOneFromConllFolder(folder):
    """
    Function making a number of post processing functions and rewriting the conll files in a new folder
    """
    if not os.path.isdir("post_traitement/"):
        os.mkdir("post_traitement/")
    files_list=os.listdir(folder)
    for file in files_list:
        with open(f"{folder}/{file}","r") as f:
            lines=f.readlines()
        lines=removeMinusOneFromConllFile(lines)
        lines=correctAmal(lines)
        rewritePostProcessedFile(lines,file)
    return True

if __name__=="__main__":
    folder=sys.argv[1]
    removeMinusOneFromConllFolder(folder)