a=[31, 14,15,7,2]
a.sort(reverse=True)
from  operator import itemgetter
d = dict()
for i in a:
    d[i] = bin(i).count("1")

w = d.items()
x = sorted(w, key=itemgetter(1),reverse=True)
print x
for i in range(0,len(x)-1):
    for j in range(i+1,len(x)):
        if (x[i][1] == x[j][1] and x[i][0] < x[j][0]):
           a=x[i];
           x[i]=x[j];
           x[j]=a;
print x;
for k in x:
    print k[0]
