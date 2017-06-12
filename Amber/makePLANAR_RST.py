#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
parser = argparse.ArgumentParser(description='''Generate the planarity restraint for the input base pair
 to be used in Amber calculation.''')
parser.add_argument('-i', help='the input file define the base pair')
parser.add_argument('-o', help='output the planarity restraints file')
parser.add_argument('-res', nargs='*', help='input residues type for base pair, eg: G 1 G 2')
args = parser.parse_args()
base_pair =args.res
input_file = args.i
output_file = args.o

def read_input_from_file(res_file):
    '''read base pair list form text file.'''
    residue_list = []
    with open(res_file) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        temp = lines[i].split()
        residue_list.append(temp)
#        else:
#            raise TypeError('Incorrect residues in line %d' %i)
    return residue_list

def base_pair_split(bp):
    '''Convert longer base pair (bp) list like this 'G 1 G 2 G 3' into 
    single base pair, 'G 1 G 2', 'G 2 G 3', 'G 3 G 1'.'''
    length = len(bp)
    if length != 2 and length%2 == 0:
        for i in range(1,length,2):
            if not bp[i].isdigit():
                raise TypeError('Incorrect base pair! Input base pair like this: G 1 G 2')
        if length == 4:
            return [bp]
        else:
            bp.append(bp[0])
            bp.append(bp[1])
            return [[bp[i],bp[i+1],bp[i+2],bp[i+3]] for i in range(0,len(bp)-2,2)]
    else:
        raise TypeError('Incorrect base pair! Input base pair like this: G 1 G 2')

#GC, AT Waston-Crick base pair
GC_AT_WC = ["N3 N1 N3 N1", "atnam(1)='N3', atnam(2)='N1', atnam(3)='N3', atnam(4)='N1'", 
                   "C6 N3 N1 C4", "atnam(1)='C6', atnam(2)='N3', atnam(3)='N1', atnam(4)='C4'", 
                   "C5 C2 C2 C5", "atnam(1)='C5', atnam(2)='C2', atnam(3)='C2', atnam(4)='C5'"]
CG_TA_WC = ["N1 N3 N1 N3", "atnam(1)='N1', atnam(2)='N3', atnam(3)='N1', atnam(4)='N3'", 
                   "C4 N1 N3 C6", "atnam(1)='C4', atnam(2)='N1', atnam(3)='N3', atnam(4)='C6'", 
                   "C5 C2 C2 C5", "atnam(1)='C5', atnam(2)='C2', atnam(3)='C2', atnam(4)='C5'"]
# GG hoogsteen base pair
GG_Hoogsteen = ["N9 N7 N1 N3", "atnam(1)='N9', atnam(2)='N7', atnam(3)='N1', atnam(4)='N3'", 
                   "C5 C2 N7 C4", "atnam(1)='C5', atnam(2)='C2', atnam(3)='N7', atnam(4)='C4'", 
                   "C2 C8 C2 C8", "atnam(1)='C2', atnam(2)='C8', atnam(3)='C2', atnam(4)='C8'"]
atom_dict = {'GG':GG_Hoogsteen, 'GC':GC_AT_WC, 'AT':GC_AT_WC,'CG':CG_TA_WC, 'TA':CG_TA_WC}

#change this to ajust your calculation.
parameters = 'rk2=20.0, rk3=20.0, nstep1=0, nstep2=200000'

def generate_restraint(base_pair):
    '''generate restraint for input base pair'''
    if len(base_pair)!=4:
        raise IndexError("base pair must be 4")
    res_key = base_pair[0]+base_pair[2]
    res1 = base_pair[0]+base_pair[1]
    res2 = base_pair[2]+base_pair[3]
    iat = ','.join([base_pair[1],base_pair[1],base_pair[3],base_pair[3]])

    s = (res1, res2, atom_dict[res_key][0], iat, parameters, atom_dict[res_key][1], \
     atom_dict[res_key][2], iat, atom_dict[res_key][3], atom_dict[res_key][4], \
     iat, atom_dict[res_key][5], res1, res2)

    restraint = '''# ----begin of planar restraint for base pair %s->%s---
#  planar restraint for :  %s
 &rst iat=%s, %s,
     r1=350.0, r2=355.0, r3=365.0, r4=370.0,
     %s, iresid=1, &end

#  planar restraint for :  %s
 &rst iat=%s, %s,
     r1=350.0, r2=355.0, r3=365.0, r4=370.0, iresid=1, &end

#  planar restraint for :  %s
 &rst iat=%s, %s,
     r1=350.0, r2=355.0, r3=365.0, r4=370.0, iresid=1, &end
# ----end of planar restraint for base pair %s->%s----\n''' 

    return restraint %s

def write_restraint_file(restraints, output_file):
    try:
        with open(output_file, 'w') as f:
            for i in restraints:
                f.write(i+'\n')
    except IOError:
        print('Unable to write restraint. Please check restraint file name or you have the right to write.')

if __name__ == '__main__':
    import sys
    restraint_list = []
    residue_list = []
    if input_file:
        residue_list  = residue_list + read_input_from_file(input_file)
    if base_pair:
        residue_list.append(base_pair)
    if len(residue_list) == 0:
        print('Unable to get residues list, exiting...')
        sys.exit()
    else:
        for bp in residue_list:
            base_pairs = base_pair_split(bp)
            for b in base_pairs:
                restraint_list.append(generate_restraint(b))
    if output_file:
        write_restraint_file(restraint_list, output_file)
        print('successfully write the restraint file: %s' %output_file)
    else:
        for i in restraint_list:
            print(i)

