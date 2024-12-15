import numpy as np
import pandas as pd
import csv

data_txtDF = pd.read_csv("/InterKG/dataset/last-fm/kg_final.txt", sep=' ', header=None, names=['h', 'r', 't'])

# Deletes triples that do not contain items
n = 48122   # items-1
row_indexes = data_txtDF[(data_txtDF['h'] > n) & (data_txtDF['t'] > n)].index

df_drop = data_txtDF.drop(row_indexes)

df1 = df_drop.pivot_table(values='t',columns='r',index='h',aggfunc=np.min)

df1.to_csv('final.csv',sep=',',index=False,header=False)


