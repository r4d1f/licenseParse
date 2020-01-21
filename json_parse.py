import json

with open('dataObrnadzor.json', encoding="utf8") as f:
    templates = json.load(f)

arr = []
for i in range(len(templates)):
    arr.append(templates[i]['guid'])
with open('file.txt', 'w') as f:
    for i in arr:
        f.write(i)
        f.write('\n')