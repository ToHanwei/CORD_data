#!coding:utf-8

import os
import sys
import pickle
import pandas as pd

from collections import defaultdict


def buildMap(mapfile):
    with open(mapfile, 'rb') as mapf:
        # key   --> seqid
        # value --> taxid
        mapdict = pickle.load(mapf)
    return mapdict


def summaryMap(mapfile):
    claded = defaultdict(list)
    data = pd.read_csv(mapfile, sep='\t')
    taxids = data['taxid'].values
    clades = data['Clade'].values
    orders = data['Order'].values
    taxids = [str(tax) for tax in taxids]
    clademap = dict(zip(taxids, clades))
    ordermap = dict(zip(taxids, orders))
    for i, clade in enumerate(clades):
        claded[clade].append(taxids[i])
    return clademap, ordermap, claded


def proceFasta(fasfile):
    with open(fasfile) as fasf:
        seqs = fasf.read().split('>')[1:]
    fasdict = {}
    for seq in seqs:
        lines = seq.split('\n')
        head = lines[0]
        aads = ''.join(lines[1:])
        fasdict[head] = aads
    return fasdict


def splitClade(seqdict, seq2tax, clademap):
    cladeout = defaultdict(list)
    for head, aads in seqdict.items():
        taxid = seq2tax[head]
        clade = clademap[taxid]
        cladeout[clade].append((head, aads))
    write2file(cladeout, 'msaSeqs')
    return cladeout


def write2file(indict, outdir):
    for name, seqs in indict.items():
        name = name.replace(' ', '_')
        name = name.replace('/', '-')
        outfile = os.path.join(outdir, name+'.fas')
        outf = open(outfile, 'w')
        for head, aads in seqs:
            line = '>' + head + '\n' + aads + '\n'
            outf.write(line)
        outf.close()


def splitOrder(seqd, seq2tax, ordermap, claded):
    for clade, seqs  in seqd.items():
        clade = clade.replace(' ', '_')
        clade = 'msaSeqs/' + clade
        os.mkdir(clade)
        orders = defaultdict(list)
        for head, aads in seqs:
            taxid = seq2tax[head]
            order = ordermap[taxid]
            orders[order].append((head, aads))
        write2file(orders, clade)


def main():
    # msa dataset
    msafile = sys.argv[1]
    # seqid map to taxid 
    seqid2taxidfile = sys.argv[2]
    # summary mapfile
    summaryfile = sys.argv[3]
    
    seqd = proceFasta(msafile)
    seq2tax = buildMap(seqid2taxidfile)
    clademap, ordermap, claded = summaryMap(summaryfile)
    cladeout = splitClade(seqd, seq2tax, clademap)
    splitOrder(cladeout, seq2tax, ordermap, claded)
    

if __name__ == "__main__":
    main()
