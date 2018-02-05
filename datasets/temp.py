import pandas as pd

df = pd.read_csv("italy_cities.csv", sep=',')

print(df)
cities = df['Name'].values

import csv
import numpy as np
fout = open("italy_prices.csv", "w")
wrt = csv.writer(fout)
wrt.writerow(['dep','arr','price'])
for idx,c in enumerate(cities):
	for j in range(idx+1,len(cities)):
		wrt.writerow([c,cities[j],np.random.randint(low=50, high=500) / 2.5])

fout.close()
