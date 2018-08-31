import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

z = np.loadtxt("temperatura_media_oraria_prisma_2016122712.txt", skiprows=6)
ax = sns.heatmap(z)

im = plt.imshow(z, cmap='inferno', aspect='auto') # pl is pylab imported a pl

plt.show()