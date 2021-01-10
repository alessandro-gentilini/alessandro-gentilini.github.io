import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.cm as cm

N_total = 87216
N_altro = 34967
N_sociosanitario = 52249
side = int(math.modf(math.sqrt(N_total))[1])

altro = np.full(N_altro,1)
sociosanitario = np.full(N_sociosanitario,2)
tutti = np.concatenate([altro,sociosanitario])
tutti.resize((side,side+1))

N_ss_IGG = 2873
N_ss_IGM = 1655
N_ss_IGG_and_IGM = 1163
N_ss_negative = N_sociosanitario-N_ss_IGG-N_ss_IGM-N_ss_IGG_and_IGM
N_ss_IGG_swab = 1267
N_ss_IGM_swab = 704
N_ss_IGG_and_IGM_swab = 696

N_a_IGG = 1627
N_a_IGM = 895
N_a_IGG_and_IGM = 637
N_a_negative = N_altro-N_a_IGG-N_a_IGM-N_a_IGG_and_IGM
N_a_IGG_swab = 743
N_a_IGM_swab = 443
N_a_IGG_and_IGM_swab = 409

swab = np.concatenate([
np.full(N_a_IGG_swab,1),
np.full(N_a_IGG-N_a_IGG_swab,2),
np.full(N_a_IGM_swab,3),
np.full(N_a_IGM-N_a_IGM_swab,4),
np.full(N_a_IGG_and_IGM_swab,5),
np.full(N_a_IGG_and_IGM-N_a_IGG_and_IGM_swab,6),
np.full(N_a_negative,7),
np.full(N_ss_IGG_swab,8),
np.full(N_ss_IGG-N_ss_IGG_swab,9),
np.full(N_ss_IGM_swab,10),
np.full(N_ss_IGM-N_ss_IGG_swab,11),
np.full(N_ss_IGG_and_IGM_swab,12),
np.full(N_ss_IGG_and_IGM-N_ss_IGG_and_IGM_swab,13),
np.full(N_ss_negative,14)
])
swab.resize((side,side+1))

siero = np.concatenate([
np.full(N_a_IGG,1),
np.full(N_a_IGM,2),
np.full(N_a_IGG_and_IGM,3),
np.full(N_a_negative,4),
np.full(N_ss_IGG,5),
np.full(N_ss_IGM,6),
np.full(N_ss_IGG_and_IGM,7),
np.full(N_ss_negative,8)])
siero.resize((side,side+1))
        
palette1 = np.array([[  255,   255,   255],
                    [    0,     0,   255],
                    [  255,     0,     0]])

RGB = palette1[tutti]
fig, ax = plt.subplots()
ax.imshow(RGB)
ax.axis('off')
ax.text(100,100,34967 (forze dell'ordine",color='white')
fig.savefig('screening.png',bbox_inches='tight')

palette2 = np.array([[  255,   255,   255],
                    [    0,    0,   255],
                    [    0,     0,   255],
                    [    0,     0,   255],
                    [    245,    245,   255],
                    [255,0,0],
                    [255,0,0],
                    [255,0,0],
                    [255,245,245]
                    ])

RGB2= palette2[siero]
fig, ax = plt.subplots()
ax.imshow(RGB2)
ax.axis('off')
fig.savefig('screening_siero.png',bbox_inches='tight')                    

palette3 = np.array([[  255,   255,   255],

                    [    0,    0,   255],
                    [    200,   200,   255],

                    [    0,    0,   255],
                    [    200,   200,   255],                    

                    [    0,    0,   255],
                    [    200,   200,   255],                    

                    [    245,    245,   255],

                    [   255,     0,   0],
                    [   255,    200,   200],

                    [   255,     0,   0],
                    [   255,    200,   200],

                    [   255,     0,   0],
                    [   255,    200,   200],                    

                    [    255,    245,   245],
                    ])

RGB3= palette3[swab]
fig, ax = plt.subplots()
ax.imshow(RGB3)
ax.axis('off')
fig.savefig('screening_swab.png',bbox_inches='tight') 