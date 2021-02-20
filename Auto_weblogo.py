#!coding:utf-8

import re
import os
import sys
from tempfile import NamedTemporaryFile

# MSA format file
msafile = sys.argv[1]
# template site
sitefile = sys.argv[2]


def make_command(label, infile, outfile):
	command = ("weblogo"
		+ " -f " + infile
		+ " -D fasta"
		+ " -A protein"
		+ " -o " + outfile
		+ " -F svg"
		+ " --annotate " + label
		+ " --show-yaxis yes"
		+ " --fineprint ''"
		+ " --rotate-numbers YES"
		+ " --color-scheme chemistry"
		+ " --stacks-per-line 100"
		+ " --number-fontsize 3.5"
		+ " --stack-width 6"
		+ " --title-fontsize 4"
		+ " --yaxis 5.5"
		+ " --fontsize 6"
		)
	return command


with open(sitefile) as sitef:
	sites = [line.strip().split()[2] for line in sitef]

with open(msafile) as msaf:
	seqs = msaf.read().split('>')[1:]

parms = [
	(0, 22), (22, 52), (52, 58),
	(58, 86), (86, 92), (92, 130),
	(130, 137), (137, 163), (163, 195),
	(195, 228), (228, 233), (233, 262),
	(262, 268), (268, 292), (292, 305),
	(305, 310)
]

names = [
	'NTERM', 'TM1', 'ICL1', 'TM2',
	'ECL1', 'TM3', 'ICL2', 'TM4',
	'ECL2', 'TM5', 'ICL3', 'TM6',
	'ECL3', 'TM7', 'H8', 'CTERM'
]

frags = [
	[], [], [], [],
	[], [], [], [],
	[], [], [], [],
	[], [], [], []
]

labels = []

for seq in seqs:
	lines = seq.split('\n')
	header = lines[0]
	aads = ''.join(lines[1:])
	for i, parm in enumerate(parms):
		frag = aads[parm[0]:parm[1]]
		frag = ">" + header + "\n" + frag + "\n"
		frags[i].append(frag)

for parm in parms:
	label = ','.join(sites[parm[0]:parm[1]])
	labels.append(label)

outfile = msafile.split('.')[0] + '.txt'
fout = open(outfile, 'w')
fout.write('fragment@@@svgstr@@@length###')
for i, frag in enumerate(frags):
	label = labels[i]
	fraglen = str(len(frag[0].split('\n')[1]))
	TempFile = NamedTemporaryFile('w+t')
	TempName = TempFile.name
	outfile = TempName + ".svg"
	TempFile.writelines(frag)
	TempFile.seek(0)
	command = make_command(label, TempName, outfile)
	os.system(command)
	svgf = open(outfile)
	svgstr = svgf.read()
	strinfo = re.compile(' width="\d{1,5}pt" height="\d{1,5}pt"')
	svgstr = strinfo.sub('', svgstr)
	svgf.close()
	os.remove(outfile)
	fout.write(names[i]+'@@@'+svgstr+'@@@'+fraglen+'###')

fout.close()
