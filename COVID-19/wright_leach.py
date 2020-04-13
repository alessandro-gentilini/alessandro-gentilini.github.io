# Appendix in 
#
# Tommy Wright
# Exact Confidence Bounds when Sampling from Small Finite Universes
# An Easy Reference Based on the Hypergeometric Distribution
# Springer Verlag 1991
#
# A SAS MACRO FOR GENERATING EXACT ONE-SIDED LOWER AND 
# UPPER CONFIDENCE BUONDS FOR A FOR STATED
# N,n,a, and 1-\alpha^{\star}
# By E. Leach, Mathematical Sciences Section, Oak Ridge National Laboratory, Oak
# Ridge, Tennessee 37831-8083. 
#
# https://link.springer.com/content/pdf/bbm%3A978-1-4612-3140-0%2F1.pdf

from scipy.stats import hypergeom
import sys

# PROBHYPR Function
# http://documentation.sas.com/?docsetId=casfedsql&docsetTarget=n0h6p8jhzwlk2jn1gvhzslxsopws.htm&docsetVersion=3.1&locale=en
def SAS_PROBHYPR(N,K,n,x):
    return hypergeom.cdf(x,N,K,n)

def wrigth_leach(NN,N,A,CF):
    ALPHA = 1-CF
    LL = 0
    UL = 0
    DONEL = False
    DONEU = False
    X1 = A-1
    for KL in range(1,NN):
        if(KL%1000==0):
            print(KL,file=sys.stderr)
        if X1 < 0:
            DONEL = True
        GOTO_NEXT = False
        if DONEL:
            GOTO_NEXT = True
        if X1 < max(0,KL+N-NN):
            GOTO_NEXT = True
        if X1 > min(KL,N):
            GOTO_NEXT = True
        if not GOTO_NEXT:
            VAL1 = 1-SAS_PROBHYPR(NN,KL,N,X1)
            if VAL1 > ALPHA and LL==0:
                LL = KL
                DONEL = True
        else:
            GOTO_CHECK = False
            if DONEU == True:
                GOTO_CHECK = True
            KU = NN - KL
            if KU < 1:
                GOTO_CHECK = True
            if A < max(0,KU+N-NN):
                GOTO_CHECK = True
            if A > min(KU,N):
                GOTO_CHECK = True
            if not GOTO_CHECK:
                VAL2 = SAS_PROBHYPR(NN,KU,N,A)
                if VAL2 > ALPHA and UL==0:
                    UL = KU
                    DONEU = True
            else:                
                if DONEL == True and DONEU == True:
                    return [LL,UL]
                


        

# Statement: select probhypr(200,50,10,2);
# Results: 0.5236734081
expected_result = "0.5236734081"
sig_figures = len(expected_result)
assert str(SAS_PROBHYPR(200,50,10,2))[0:sig_figures] == expected_result

assert wrigth_leach(46,1,0,.95) == [0,43]
assert wrigth_leach(185,53,3,.95) == [4,23]
assert wrigth_leach(2000,200,40,.975) == [299,518]

assert wrigth_leach(1200,120,3,.95) == [9,73]
assert wrigth_leach(3300,300,49,.99) == [393,714]