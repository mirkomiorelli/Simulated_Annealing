# Import libraries
import pandas as pd
import numpy as np
import sys
sys.path.append('../cpp/')
import lib_anneal as lann
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
np.random.seed(0)


# Print map of cities function
def print_map_world(df, s):
    fig, ax = plt.subplots(figsize=(20,14))

    earth = Basemap(resolution='l', projection='mill')
    earth.drawcoastlines(color='0.50', linewidth=0.25)
    earth.fillcontinents(color='0.95')

    for i,r in df.iterrows():
        x, y = earth(r['Lon'],r['Lat'])
        earth.plot(x, y, 'o', markersize=4, markerfacecolor='red', markeredgecolor='black', alpha=0.8)

    x, y = earth(np.array(df['Lon'])[s],np.array(df['Lat'])[s])
    earth.plot(x,y,lw=0.5,color='blue',alpha=1.0)
    plt.show()


# Read data, create x and y coordinate variables and 
# N which is the total number of cities
df = pd.read_csv('../datasets/world_cities.csv').drop_duplicates(subset='Name')
N = len(df)
x = np.array(df['Lon'])
y = np.array(df['Lat'])
print(df.head())


# Now create the lookup-table for the distances
# Extract cities names
cities = df['Name'].values
# Preallocate look-up table
dtable = [[0.0 for c in cities] for c in cities]
# Calculate distances
fin = open('world_cities_dtable.csv','r')
for line in fin:
	line = line.rstrip('\n').split(',')
	dtable[int(line[0])][int(line[1])] = float(line[2])
fin.close()

#fout = open('world_cities_dtable.csv','w')
#for i, ci in enumerate(cities):
#    for j, cj in enumerate(cities):
#        delta_lon = df.loc[df['Name'] == ci, 'Lon'].values - df.loc[df['Name'] == cj, 'Lon'].values
#        delta_lat = df.loc[df['Name'] == ci, 'Lat'].values - df.loc[df['Name'] == cj, 'Lat'].values
#        dtable[i][j] = float(np.sqrt(delta_lon**2 + delta_lat**2))
#        fout.write(str(i) + ',' + str(j) + ',' + str(dtable[i][j]) + '\n')
#fout.close()

# Now we normalize all the distances from 0 to 1
dmax = np.max(dtable)
dmin = np.min(dtable)
dtable = [[(x - dmin) / (dmax - dmin) for x in r] for r in dtable]

# Create mapping city-id to setup prices table
mapping = {}
imapping = {}
for idcity,cname in enumerate(cities):
    # mapping: name -> id
    mapping[cname] = idcity
    # inverse mapping: id -> name
    imapping[idcity] = cname
# Set seed for reproducibility of the results
np.random.seed(27)
# Initialize state (path)
s = np.arange(N)
np.random.shuffle(s)
# Append first city id to end of path (we need a closed path!)
s = np.append(s,s[0])
print(s)
print([imapping[idc] for idc in s])


# Set parameters
T = 1.0
iter_max = 2000
alpha = 1.0
ptable = [[]]
# Simulate annealing
sold = s
slist = []
for i in range(500):
    rd = np.random.randint(low=0,high=1000)
    s, l_arr, T, accepted, rejected = lann.anneal_double(dtable, ptable, alpha, s, N, T, iter_max, 0, True)
    #if i % 100 == 0:
    T = 0.9999 * T
    #if i % 100 == 0:
    slist.append(s)



# PLOT

fig, ax = plt.subplots(figsize=(10,7))

earth = Basemap(resolution='l', projection='mill')
earth.drawcoastlines(color='0.50', linewidth=0.25)
earth.fillcontinents(color='0.95')

for i,r in df.iterrows():
	x, y = earth(r['Lon'],r['Lat'])
	earth.plot(x, y, 'o', markersize=4, markerfacecolor='red', markeredgecolor='black', alpha=0.8)


txt = ax.annotate('0', xy=(0.1, 0.9), xycoords='axes fraction')
#plt.show(block=False)

for idx,s in enumerate(slist):
    x, y = earth(np.array(df['Lon'])[s],np.array(df['Lat'])[s])
    if idx == 0:
        line, = earth.plot(x,y,lw=0.5,color='blue',alpha=1.0)
    else:
        line.set_xdata(x)
        line.set_ydata(y)
        fig.canvas.update()
        fig.canvas.flush_events()
        txt.set_text(str(idx*2000))
        plt.savefig('{0:05d}'.format(idx) + '.png', bbox_inches = 'tight')
    plt.savefig('{0:05d}'.format(idx) + '.png', bbox_inches='tight')

import imageio
import os
with imageio.get_writer('test_world.gif', mode='I', duration=0.06) as writer:
    for idx in range(len(slist)):
        filename = '{0:05d}'.format(idx) + '.png'
        image = imageio.imread(filename)
        writer.append_data(image)
        os.remove(filename)
writer.close()
