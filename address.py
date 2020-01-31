import re

def f(lines):
	lines = lines.split(',')
	for j in range(len(lines)):
		lines[j] = lines[j].strip(' ')
	for j in range(len(lines)): 
		if (lines[j].isdigit()) & (len(lines[j]) > 4) & (j != 0):
			tmp = lines[0]
			lines[0] = lines[j]
			lines[j] = tmp
		if ((re.search(r'г\.', lines[j]) != None) | (re.search(r'с\.', lines[j]) != None) |\
		(re.search(r'пгт', lines[j]) != None) | (re.search(r'пос\.', lines[j]) != None) |\
		(re.search(r'город', lines[j]) != None) | (re.search(r'п\.', lines[j]) != None) & (j != 1)) & (len(lines) > 1):
			tmp = lines[1]
			lines[1] = lines[j]
			lines[j] = tmp
		if ((re.search(r'ул\.', lines[j]) != None) | (re.search(r'пер\.', lines[j]) != None) |\
		(re.search(r'пл\.', lines[j]) != None) | (re.search(r'переулок', lines[j]) != None) |\
		(re.search(r'просп\.', lines[j]) != None) | (re.search(r'туп\.', lines[j]) != None) & (j != 2)) & (len(lines) > 2):
			tmp = lines[2]
			lines[2] = lines[j]
			lines[j] = tmp
		if ((re.search(r'д\.', lines[j]) != None) | ((lines[j].isdigit()) & (len(lines[j]) <= 4)) & (j != 3)) & (len(lines) > 3):
			tmp = lines[3]
			lines[3] = lines[j]
			lines[j] = tmp
	for j in range(len(lines)): 
		if (re.search(r'[Рр]ос*сия', lines[j]) != None) | (re.search(r'РФ', lines[j]) != None) |\
		(re.search(r'область', lines[j]) != None) | (re.search(r'район', lines[j]) != None):
			lines[j] = ''
	while '' in lines:
		lines.remove('')
	for j in range(len(lines)-1):
		lines[j] += ', '
	return(''.join(lines))