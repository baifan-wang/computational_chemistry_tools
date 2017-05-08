#!/usr/bin/env python3.5
import sys

__author__ = 'Baifan Wang'
'''uasge: python gautopdb.py gaussian.log name.pdb'''

atomtype = {'1':'H', '2':'He', '3':'Li', '4':'Be', '5':'B', '6':'C', '7':'N', '8':'O', '9':'F', '10':'Ne',
'11':'Na', '12':'Mg', '13':'Al', '14':'Si', '15':'P', '16':'S', '17':'Cl', '18':'Ar', '19':'K', '20':'Ca',
'21':'Sc', '22':'Ti', '23':'V', '24':'Cr', '25':'Mn', '26':'Fe', '27':'Co', '28':'Ni', '29':'Cu', '30':'Zn',
'31':'Ga', '32':'Ge', '33':'As', '34':'Se', '35':'Br', '36':'Kr', '37':'Rb', '38':'Sr', '39':'Y', '40':'Zr',
'41':'Nb', '42':'Mo', '43':'Tc', '44':'Ru', '45':'Rh', '46':'Pd', '47':'Ag', '48':'Cd', '49':'In', '50':'Sn',
'51':'Sb', '52':'Te', '53':'I', '54':'Xe', '55':'Cs', '56':'Ba', '57':'La', '58':'Ce', '59':'Pr', '60':'Nd', 
'61':'Pm', '62':'Sm', '63':'Eu', '64':'Gd', '65':'Tb', '66':'Dy', '67':'Ho', '68':'Er', '69':'Tm', '70':'Yb', 
'71':'Lu', '72':'Hf', '73':'Ta', '74':'W', '75':'Re', '76':'Os', '77':'Ir', '78':'Pt', '79':'Au', '80':'Hg', 
'81':'Tl', '82':'Pb', '83':'Bi', '84':'Po', '85':'At', '86':'Rn', '87':'Fr', '88':'Ra', '89':'Ac', '90':'Th', 
'91':'Pa', '92':'U', '93':'Np', '94':'Pu', '95':'Am', '96':'Cm', '97':'Bk', '98':'Cf', '99':'Es', '100':'Fm', 
'101':'Md', '102':'No', '103':'Lr', '104':'Rf', '105':'Db', '106':'Sg', '107':'Bh', '108':'Hs', '109':'Mt', 
'110':'Ds', '111':'Rg', '112':'Cn', '114':'Fl', '116':'Lv', '118':'Uuo'}

def gaussian_log_reader(gaulog):
    try:
        with open(gaulog, 'r') as f:
            for line in f:
                yield line
    except IOError as e:
        print('Unable to open file, please check')
        sys.exit()

def extract_coordinates(gaulines, key='Input orientation:'):
    coor = []
    model = -1
    mark = False
    i = 0
    l = 0
    for line in gaulines:
        i += 1
        if line.strip() == key:  # 'Input orientation:' or 'Standard orientation'
            model += 1
            coor.append([])
            l = i + 5
            print('coordinates set: %d found in line %d' %(model+1,l))
        if i == l:
            lines = line.split()
            if lines[0].isdigit():
                coor[model].append([lines[0], atomtype[lines[1]], lines[3], lines[4], lines[5]])
            l += 1
            if line[1] == '-':
                l = 0
    if coor:
        return coor
    else:
        return None

def topdb(coor_list, pdb):
    atype = 'ATOM'
    res = 'MOL'
    chain = 'A'
    seq = '1'
    space = ''
    occu = 1.00
    bfactor = 0.00
    charge = ' '
    segment_indent = ' '
    with open(pdb, 'w') as f:
        for model in range(len(coor_list)):
            s = 'MODEL'+str(model+1).rjust(6)+'\n'
            f.write(s)
            for l in coor_list[model]:
                number = l[0]
                name = l[1]+l[0]
                if len(name) <4:
                    name = ' ' + name.ljust(4)
                else:
                    name = name.ljust(4)
                x = float(l[2])
                y = float(l[3])
                z = float(l[4])
                ele = l[1]
                s = "%s%5s %s%3s %1s%3s%s    %8.3f%8.3f%8.3f%6.2f%6.2f      %4s%2s%2s"  \
                    %(atype.ljust(6), number, name, res.rjust(3), chain, \
                    space ,seq, x, y, z, occu, bfactor, segment_indent.ljust(4), \
                    ele.rjust(2) , charge)
                f.write(s+'\n')
            end = 'ENDMDL'.ljust(80)+'\n'
            f.write(end)
        print('successfully write pdb: %s' %pdb)

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('please provide a gaussian log file and a pdb filename.')
        sys.exit()
    else:
        pass
    result = extract_coordinates(gaussian_log_reader(sys.argv[1]))
    if result == None:
        result = extract_coordinates(gaussian_log_reader(sys.argv[1]), 'Standard orientation:')
    if result == None:
        print('No coordinates were found!')
    else:
        topdb(result, sys.argv[2])
