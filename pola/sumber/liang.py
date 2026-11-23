import re
class Hyph:
    def __init__(self, patterns, exceptions=(), left=2, right=2):
        self.t = {}
        for p in patterns:
            letters = re.sub(r'\d', '', p)
            pts = [0]*(len(letters)+1); i=0
            for ch in p:
                if ch.isdigit(): pts[i]=int(ch)
                else: i+=1
            self.t[letters]=pts
        self.exc = {e.replace('-','').lower(): e.lower() for e in exceptions}
        self.left, self.right = left, right
    def points(self, w):
        lw = w.lower()
        if lw in self.exc:
            e=self.exc[lw]; res=[]; i=0
            for ch in e:
                if ch=='-': res.append(i)
                else: i+=1
            return [p for p in res if self.left<=p<=len(w)-self.right]
        word='.'+lw+'.'; pts=[0]*(len(word)+1)
        for i in range(len(word)):
            for j in range(i+1,len(word)+1):
                p=self.t.get(word[i:j])
                if p:
                    for k,v in enumerate(p): pts[i+k]=max(pts[i+k],v)
        return [i for i in range(self.left, len(w)-self.right+1) if pts[i+1]%2]
    def hyph(self, w, sep='-'):
        ps=self.points(w); out=''; last=0
        for p in ps: out+=w[last:p]+sep; last=p
        return out+w[last:]
def load_tex(path):
    s=open(path,encoding='utf8').read()
    s=re.sub(r'%.*','',s)
    pat=re.search(r'\\patterns\{(.*?)\}',s,re.S).group(1).split()
    m=re.search(r'\\hyphenation\{(.*?)\}',s,re.S)
    exc=m.group(1).split() if m else []
    return pat,exc
def load_dic(path):
    lines=open(path,encoding='latin-1').read().split('\n')
    enc=lines[0].strip(); 
    if enc.upper()=='UTF-8': lines=open(path,encoding='utf8').read().split('\n')
    pats=[]; left=right=2
    for l in lines[1:]:
        l=l.strip()
        if not l or l.startswith('%'): continue
        if l.startswith('LEFTHYPHENMIN'): left=int(l.split()[1]); continue
        if l.startswith('RIGHTHYPHENMIN'): right=int(l.split()[1]); continue
        if l.isupper() and ' ' in l: continue
        pats.append(l)
    return pats,left,right
