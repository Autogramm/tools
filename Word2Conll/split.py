corpus_part = None
#on ouvre le fichier contenant le corpus complet
with open ("sungwadia.txt", "r", encoding="utf-8") as corpus:
    count = 0
    text = corpus.readlines()
    #les parties du corpus sont délimitées par une ligne de tirets
    index = [idx for idx, s in enumerate(text) if '-------------------------------------------' in s][0]
    #on supprime tout ce qui se trouve avant le premier délimiteur
    del text[:index]
    #on crée une liste qui contiendra chaque partie du corpus
    c_part = []
    #on parcourt les lignes du texte
    for part in text:
        #tant qu'on ne rencontre pas le délimiteur, on ajoute la ligne dans la liste
        if '-------------------------------------------' not in part:
                c_part.append(part)
        #si on rencontre le délimiteur, la partie est finie: 
        else:
            with open (f'sungwadia_corpus{count}.txt', 'w', encoding='utf-8') as corpus_part:
            #on écrit les lignes de la partie dans un fichier
                corpus_part.write(' '.join(c_part))
            count += 1
            #on réinitialise la liste pour la prochaine partie
            c_part = []
            