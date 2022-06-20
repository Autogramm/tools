from lxml import etree as ET
import glob, os, re, io

#chemin du répertoire où se trouvent les fichiers XML à convertir
path = './XML'

#on parcourt le répertoire de fichiers XML
for filename in glob.glob(os.path.join(path, '*.xml')):
    count = re.findall('[0-9]+', filename)[0]
    with open (f"sungwadia_{count}.conllu", "w", encoding="utf-8") as output:
        file = f'sungwadia_{count}.xml'
        #on parse le fichier XML
        tree = ET.parse(filename)
        root = tree.getroot()
        title = ''
        for t in root.findall("item[@type='title']"):
            title += str(t.text)
            title = title.replace(" ", "_")
        for phrase in root.iter('phrase'):
            conll = []
            conll.append(title)
            for sent_id in phrase.findall("item[@num]"):
                numb = sent_id.get('num')
                conll.append(str(numb))
            text=""
            for morph in phrase.iter("morph"):
                line = ""
                for num in morph.findall("item[@num]"):
                    identifiant = num.get('num')
                    line += str(identifiant) 
                    line += '\t'
                for item in morph.findall("item[@type='txt']"):
                    line += 2* (str(item.text) + '\t')
                    #line += '\t'
                line += 6*('_\t')
                for gloss in morph.findall("item[@type='gls']"):
                    line += 'Gloss=' + str(gloss.text)   
                conll.append(line)
                conll.append('\n')
            for translation in phrase.findall("item[@type='ft']"):
                conll.append(str(translation.text))
            output.write("# sent_id = " + conll[0] + conll[1] + "\n")
            output.write("# text_en = " + conll[-1] + "\n")          
            for i in range(2, len(conll)-2):
                output.write(conll[i])
            output.write("\n")
            output.write("\n")