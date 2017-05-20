#!/usr/bin/env python3

"""
Replace the bfactor column of a pdb file from a data file.  If a data file is supplied, it reads
atom number/b-factor pairs and places the values in the b-factor column of a pdb file. Test on Amber
generate pdb and B-factor file.

usage:  python pdb_re_bfactor.py xxx.pdb  bfactor.file
"""
__author__='Baifan Wang'

def file_loader(file):
    """load the file and return the lines"""
    try:
        with open(file) as f:
            lines = f.readlines()
    except:
        print('Could not open pdb file!')
        raise
    return lines

def replace_bfactor(pdb_file, bfactor_file):
    pdb = file_loader(pdb_file)
    bfactor = file_loader(bfactor_file)
    i = 0
    l = 1
    new_pdb_file = pdb_file[:-4]+'_new.pdb'
    new_pdb = open(new_pdb_file, 'w')
    while i <len(pdb) and l<len(bfactor):
        bn =  int(float(bfactor[l].split()[0])) #atom serial number in b-factor file
        new_bfactor = float(bfactor[l].split()[1])
        if pdb[i].startswith('ATOM') or pdb[i].startswith('HETATM'):
            pn = int(pdb[i][6:11])   #atom serial number in pdb
        else:
            new_pdb.write(pdb[i])
        if bn == pn:
            if new_bfactor>=100.0:  #trunct the bfactor to less than 100.
                new_bfactor=99.99
            s = '%.2f' %new_bfactor
            s = s.rjust(5)
            new_line = pdb[i][:61] +s+pdb[i][66:]
            new_pdb.write(new_line)
            i += 1
            l += 1
        else:
            i += 1
    while i <len(pdb):  #sometime there are remainging lines
        new_pdb.write(pdb[i])
        i += 1
    new_pdb.close()
    print('The new pdb file "%s" has been generated!' %new_pdb_file)

if __name__=='__main__':
    import sys
    if len(sys.argv) !=3:
        print("usage: python pdb_re_bfactor.py  xxx.pdb  bfactor.file")
    pdb_file  = sys.argv[1]
    bfactor_file = sys.argv[2]
    replace_bfactor(pdb_file, bfactor_file)