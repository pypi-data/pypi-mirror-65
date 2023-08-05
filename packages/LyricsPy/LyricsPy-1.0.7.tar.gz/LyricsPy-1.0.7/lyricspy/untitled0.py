from json import load

with open('a.json') as f:
    a = load(f)
    
b = '\n'.join([x['description'] for x in a['lyrics']['translation']['list']])
print(b)