import sys; sys.path.insert(0, sys.argv[1])
from aturan_id import Analyzer
A=Analyzer(open('stems.txt').read().split())
words=set(open('forms_clean.txt').read().split())|set(open('gen_forms.txt').read().split())|set(open('stems.txt').read().split())
n=0
with open('latih.txt','w') as f:
    for w in sorted(words):
        if len(w)<4 or len(w)>30: continue
        if A.best(w) is None: continue
        h=A.hyph(w)
        f.write(h+'\n'); n+=1
print(n)
