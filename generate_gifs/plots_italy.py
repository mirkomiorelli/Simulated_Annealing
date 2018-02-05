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
def print_map(lon, lat, s=[]):
    fig, ax = plt.subplots(figsize=(10, 7))
    m = Basemap(resolution='l',  # c, l, i, h, f or None
                projection='merc',
                lat_0=10.8, lon_0=12.37,
                llcrnrlon=6.59, llcrnrlat=36.42, urcrnrlon=18.96, urcrnrlat=47.22)
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
    m.drawcoastlines()
    for i in range(len(df)):
        x, y = m(lon[i], lat[i])
        m.plot(x, y, 'o', markersize=8, color='red', alpha=0.8)
    x, y = m(lon[s], lat[s])
    m.plot(x, y, lw=2.0, alpha=1.0)
    # plt.savefig('local_optimum.png', bbox_inches='tight')
    plt.show()

    return


# Read data, create x and y coordinate variables
df = pd.read_csv("../datasets/italy_cities.csv")
N = len(df)
x = np.array(df['Lon'])
y = np.array(df['Lat'])
print(df.head())
# Initialize state (path)
s = np.arange(N)
np.random.shuffle(s)
# Append first city id to end of path (we need a closed path!)
s = np.append(s,s[0])
print(s)
print(df.loc[s,'Name'].values)
np.random.seed(36)
# Set parameters
iter_max = 200000 # Number of iterations
T = 1.0           # Initial temperature
# Simulate annealing
sold = s
slist = []
for i in range(200000):
    rd = np.random.randint(low=0,high=200000)
    s, l_arr, T, accepted, rejected = lann.anneal(x, y, s, T, 1, rd, True)
    if i % 100 == 0:
        T = 0.999 * T
    if i % 100 == 0:
        slist.append(s)
lon = x
lat = y

# PLOT

fig, ax = plt.subplots(figsize=(5.,3.5))
m = Basemap(resolution='l',  # c, l, i, h, f or None
                projection='merc',
                lat_0=10.8, lon_0=12.37,
                llcrnrlon=6.59, llcrnrlat=36.42, urcrnrlon=18.96, urcrnrlat=47.22)
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()
for i in range(len(df)):
    x, y = m(lon[i], lat[i])
    m.plot(x, y, 'o', markersize=4, color='red', alpha=0.8)
txt = ax.annotate('0', xy=(0.1, 0.9), xycoords='axes fraction')
#plt.show(block=False)

for idx,s in enumerate(slist):
    x, y = m(lon[s], lat[s])
    if idx == 0:
        line, = m.plot(x, y, lw=1.0, alpha=1.0, color='blue')
    else:
        line.set_xdata(x)
        line.set_ydata(y)
        fig.canvas.update()
        fig.canvas.flush_events()
        txt.set_text(str(idx*100))
        plt.savefig('{0:05d}'.format(idx) + '.png', bbox_inches = 'tight')
    plt.savefig('{0:05d}'.format(idx) + '.png', bbox_inches='tight')

import imageio
import os
with imageio.get_writer('test.gif', mode='I', duration=0.01) as writer:
    for idx in range(len(slist)):
        filename = '{0:05d}'.format(idx) + '.png'
        image = imageio.imread(filename)
        writer.append_data(image)
        os.remove(filename)
writer.close()