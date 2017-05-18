#!/usr/bin/env python3

"""
A script data to extract sequence from pdb and returns sequence information FASTA format.
It will try to read SEQRES entries; otherwise it will extract sequence information in Atom section.

Usage:  python pdbtoseq.py xxx.pdb
"""
import os, sys
__author__='Baifan Wang'

#for the convertion of residues code from three or two letter to standard one letter.
residue_dict = {
# for amino acid residues
"ALA":"A",
"ARG":"R",
"ASN":"N",
"ASP":"D",
"ASX":"B",
"CYS":"C",
"GLU":"E",
"GLN":"Q",
"GLX":"Z",
"GLY":"G",
"HIS":"H",
"ILE":"I",
"LEU":"L",
"LYS":"K",
"MET":"M",
"PHE":"F",
"PRO":"P",
"SER":"S",
"THR":"T",
"TRP":"W",
"TYR":"Y",
"VAL":"V",
"SEC":"U",
"PYL":"O",
"MSE":"M",
# for DNA residues
"DT":"T",
"DA":"A",
"DC":"C",
"DG":"G",
# for RNA residues
"U":"U",
"A":"A",
"C":"C",
"G":"G"}

def pdb_reader(pdb):
    try:
        with open(pdb) as f:
            lines = f.readlines()
    except:
        print('Could not open pdb file!')
        raise
    return lines

def SEQRES_reader(pdb):
    lines = pdb_reader(pdb)
    sequences = {}  #a dict contain {'chain':'sequence'}, like this {'A':['TTAGGG'], 'B':['GGGCCC']}
    for line in lines:
        #seqres line ='SEQRES   1 A  504  MET ALA PRO SER ALA GLY GLU ASP LYS HIS SER SER ALA'
        if line[:6] == 'SEQRES':
            temp = line.split()
            if temp[2] not in sequences:
                sequences[temp[2]] = []
            for seq in temp[4:]:
                sequences[temp[2]].append(residue_dict.get(seq, 'X'))
    return sequences

def extrect_seq(pdb):
    lines = pdb_reader(pdb)
    sequences = {}
    for line in lines:
        #atom line = "ATOM      1  N   ALA A  13      -6.757  17.096   7.497  1.00 61.00           N "
        if line[:4] == 'ATOM' or line[:6] == 'HETATM': 
            seq, chain, res = line.split()[3:6]  # residues type, chain number, residue number
            if chain not in sequences:
                sequences[chain] = []
            else:
                sequences[chain].append((res, residue_dict.get(seq, 'X')))
    for chain in sequences:
        sequences[chain] = [i[1] for i in sorted(list(set(sequences[chain])),key = lambda x:int(x[0]))]
    return sequences

def write_fasta(pdb, sequences):
    name = os.path.split(pdb)[1][:-4]
    chains = sorted([i for i in sequences])
    fasta_file = name+'.fasta'
    with open(fasta_file, 'w') as f:
        for i in chains:
            fasta_id = '>'+name+':'+i+'|PDBID|CHAIN|SEQUENCE'
            f.write(fasta_id +'\n')
            sequence = ''.join(sequences[i])
            i = 0
            while i+80 <len(sequence): #the maximum length of the line in fasta file is 80
                f.write(sequence[i:i+80]+'\n')
                i+=80
            f.write(sequence[i:] +'\n')
    return True, fasta_file
    
if __name__=='__main__':
    if len(sys.argv) != 2:
        print('Usage: python pdbtoseq.py xxx.pdb')
        sys.exit()
    elif sys.argv[1][-3:] !='pdb':
        print('Usage: python pdbtoseq.py xxx.pdb')
        sys.exit()
    sequences = SEQRES_reader(sys.argv[1])
    if len(sequences) == 0:
        sequences = extrect_seq(sys.argv[1])
    if len(sequences) == 0:
        print('No sequence information found in this pdb. Please check.')
        sys.exit()
    successful, fasta = write_fasta(sys.argv[1], sequences)
    if successful:
        print('Sucessfully write the sequence file: %s' %fasta)
    else:
        print('Cannot wirte fasta file. Please check.')