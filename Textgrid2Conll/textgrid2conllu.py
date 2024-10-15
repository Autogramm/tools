import sys
from praatio import textgrid

## The two inputs files were not using the same columns, delta is used to align.

# base_name = "nar_RouDes_2017_04_26_001_yrk-tun"
# delta = 0
base_name = "nar_RouDes_2017_04_26_002_yrk-tun"
delta = 1

input = f"Tundra_nenets/{base_name}"

tg = textgrid.openTextgrid(f'{input}.TextGrid', False)
intervals = list(tg.getTier('yrk-word'))
with open (f'{input}.tsv',"r") as f:
	data = f.readlines()

def clean_token(t):
	return (t.lower().replace('"','').replace('-','').replace('.','').replace(',',''))
def is_same_word(w1, w2):
	return clean_token (w1) == clean_token (w2)

current_interval = 0
def get_next_interval(word):
	global current_interval
	while '<' in intervals[current_interval].label: current_interval += 1
	interval = intervals[current_interval]
	if not (is_same_word(interval.label, word.lower())):
		print (f"WARNING : word = >>>{word}<<<, interval.label = >>>{interval.label}<<<")
	current_interval += 1
	return (interval.start*1000, interval.end*1000)

id = 0
sent_id = 0
for (num,line) in enumerate(data[2-delta:]):
	cols = line.split('\t')
	cols[8+delta] = cols[8+delta].strip()
	if all(x == '' for x in cols):
		print ()
	if cols[0+delta] != "":
		id = 0
		sent_id += 1
		if delta == 1:
			print (f'# sent_id = {base_name}__{cols[0]}')
		else:
			print (f'# sent_id = {sent_id}')
		print (f'# sound_url = https://grew.fr/audio/{base_name}.wav')
		print (f'# text = {cols[0+delta]}')
		print (f'# text_ru = {cols[7+delta]}')
		print (f'# text_en = {cols[8+delta].strip()}')
	if cols[2+delta] != "":
		glosses = cols[4+delta].split('-')
		morphs = cols[2+delta].split('-')
		word = cols[1+delta]
		(start, end) = get_next_interval (word)
		for (i,m) in enumerate(morphs):
			id += 1
			morph = m if i == 0 else '-'+m
			lemma = cols[3] if i == 0 else '_'
			pos = cols[5] if i == 0 else 'X'
			gloss = glosses[i] if len(glosses) == len(morphs) else "TODO"
			print (f'{id}\t{morph}\t{lemma}\t{pos}\t_\t_\t_\t_\t_\tAlignBegin={start}|AlignEnd={end}|Gloss={gloss}')
print ()
