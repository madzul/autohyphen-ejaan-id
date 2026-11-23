import sys
stems=[w for w in open('stems.txt').read().split() if len(w)>=3]
def meN(s, base):  # base 'me' or 'pe'
    c=s[0]
    if c in 'aeioughkq' or s[:2]=='kh':
        return base+'ng'+(s[1:] if c=='k' and s[:2]!='kh' and len(s)>3 else s)
    if c in 'bfv': return base+'m'+s
    if c=='p': return base+'m'+s[1:]
    if c in 'dcjz': return base+'n'+s
    if c=='t': return base+'n'+s[1:]
    if c=='s' and s[:2]!='sy': return base+'ny'+s[1:]
    return base+s
out=set()
SUF=['','kan','an','i','nya','kannya','annya','inya']
for s in stems:
    pres=[s, 'di'+s, 'ter'+s, 'ber'+s, 'ke'+s, 'se'+s, 'per'+s, 'memper'+s, 'diper'+s, meN(s,'me'), meN(s,'pe')]
    for p in pres:
        for x in SUF:
            out.add(p+x)
print(len(out), file=sys.stderr)
open('gen_forms.txt','w').write('\n'.join(sorted(out))+'\n')
