#!/usr/bin/env python3.5
import os, sys

"""
A script to split each model of pdb into separate pdb file.

Usage:  python splitnmr.py xxx.pdb
"""
__author__='Baifan Wang'

def splitnmr(pdb):
    name = os.path.splitext(pdb)[0]
    try:
        with open(pdb) as f:
            lines = f.readlines()
    except:
        print('Could not open pdb file!')
        raise
    i = 0
    m_start, m_end = [], []  #record the position of the 'Model' and 'ENDMDL' line
    for line in lines:
        if line[:5] == 'MODEL':
            m_start.append(i)
        elif line[:6] == 'ENDMDL':   #find the position where model ends.
            m_end.append(i)
        i += 1
    if len(m_start) == 0:
        raise ValueError('There is not structure models in pdb!')
    for l in range(0, len(m_start)):
        pdb_number = '_%02d.pdb' %(l+1)
        split_pdb = name + pdb_number
        with open(split_pdb, 'w') as f:
            for line in lines[m_start[l]:m_end[l]+1]:
                f.write(line)
    return len(m_start)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage:  python splitnmr.py xxx.pdb')
        sys.exit()
    pdb = sys.argv[1]
    num_model = splitnmr(pdb)
    print("Successfully generated %d models from %s'" %(num_model, pdb))
