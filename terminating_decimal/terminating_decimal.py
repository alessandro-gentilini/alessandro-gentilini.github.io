from symbol import while_stmt

from sympy.ntheory import factorint
import numpy as np
import matplotlib.pyplot as plt

def is_terminating_denom(d):
    return factorint(d).keys() == [2, 5] or factorint(d).keys() == [2] or factorint(d).keys() == [5]

def get_n(sz):
    nr = sz
    nc = sz
    m = np.zeros((nr + 1, nc + 1))
    n = 0
    tot = 0
    for r in range(1, m.shape[0]):
        for c in range(1, m.shape[1]):
            tot = tot + 1
            term = is_terminating_denom(c) or r % c == 0
            m[r, c] = term
            if term:
                n = n + 1
    return tot-n

#for sz in range(1,10):
#    print(sz,get_n(sz))

def get_period_length(n,m):
    k = 1
    while (10**k-1)*n % m != 0:
        k = k + 1
    return k

nr = 30
nc = 30
m = np.zeros((nr+1,nc+1))
m2 = np.zeros((nr+1,nc+1))
n = 0
for r in range(1, m.shape[0]):
    for c in range(1, m.shape[1]):
        term = is_terminating_denom(c) or r%c==0
        m[r, c] = term
        print(r, c, term)
        if term:
            n = n + 1
        if not term:
            m2[r,c]=get_period_length(r,c)

print(n)

plt.imshow(m)
plt.xlabel(r'$c$')
plt.ylabel(r'$r$')
plt.title(r'$\frac{r}{c}$ is a terminating decimal')
plt.colorbar()
plt.show()