import complexity_science.ca as cs
import numpy as np
import pandas as pd

mapsize = [4,4]
gammalist = np.linspace(0,1,10)
results = pd.DataFrame() 
cols = []

for gamma in gammalist:
    cols.append(gamma)
    mpa = cs.mpa([8,8], gamma=gamma)
    #print(mpa.run_collect(10000).mean)
    results[gamma] = mpa.run_collect(15000)['mean']
    #results.append(mpa.run_collect(15000, steady_state=True))
    
results.to_csv('ns.csv')
#df = pd.DataFrame(results, columns=cols)
#print(df)
#df.to_csv('ns.csv')
