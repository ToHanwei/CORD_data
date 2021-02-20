#!coding: utf-8

import sys
import pandas as pd
from collections import Counter

# MSA output format file
msafile = sys.argv[1]

# config
names = [
	'M', 'A', 'I', 'L', 'V',
	'W', 'Y', 'F',
	'N', 'Q', 'S', 'T',
	'H', 'R', 'K',
	'D', 'E',
	'G', 'P', 'C',
	'HA', 'HR', 'HB', 'CP', 'CN'
	]

msadict = {}
with open(msafile) as msaf:
	seqs = msaf.read().split('>')[1:]

num_seqs = len(seqs)

for seq in seqs:
	lines = seq.strip().split('\n')
	key = lines[0]
	aad = ''.join(lines[1:])
	msadict[key] = aad

sites = list(zip(*msadict.values()))
sites = [Counter(site) for site in sites]

cons = []
for site in sites:
	v = sorted(site.items(), key=lambda x: x[1], reverse=True)
	if v[0][0] != "-":
		con = v[0][0]
	else:
		con = v[1][0]
	cons.append(con)
	site['HA'] = site['M'] + site['A'] + site['I'] + site['L'] + site['V']
	site['HR'] = site['W'] + site['Y'] + site['F']
	site['HB'] = site['N'] + site['Q'] + site['S'] + site['T']
	site['CP'] = site['H'] + site['K'] + site['R']
	site['CN'] = site['D'] + site['E']
	#site['consensues'] = con

df = pd.DataFrame.from_dict(sites)
df = (df / num_seqs) * 100
df = df[names]
df.index = range(1, 311)
df = df.round(2)
df.fillna(0, inplace=True)
df['consensues'] = cons
#points = [(309-i, j, df.iloc[i][j]) for i in range(310) for j in range(25)]

df.to_csv("test.csv", index=False)
