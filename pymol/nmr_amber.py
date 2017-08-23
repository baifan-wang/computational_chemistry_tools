'''
# Pymol Script: For visualizing the NMR constrains (Amber format), on the calculated structure. 
# Author: Baifan Wang
# Usage:
# load pdb file.
# in the command, type:
# run nmr_amber.py
# and then type:
# load_amber('restraint_file')
'''
from __future__ import print_function
def load_amber(amber):
    with open(amber,'r') as f:
        lines = f.readlines()
    at1, at2 = '',''
    alist = []
    for line in lines:
        if line.startswith('  ixpk'):  #get atomic id
            at1, at2 = line.split(',')[2].split()[1].strip(), line.split(',')[3].strip()
            if at1 !='-1' and at2 !='-1':
                alist.append([at1, at2])
        elif at1 == '-1' and line.startswith(' igr1'): # usually it is a methyl group
            at1 = line.split(',')[0].split()[1].strip()
            at1 = str(int(at1)-1) #using carbon atom id instead
            if at2 != '-1':
                alist.append([at1, at2])
        elif at2 == '-1' and line.startswith(' igr2'):
            at2 = line.split(',')[0].split()[1].strip()
            at2 = str(int(at2)-1)
            if at1 != '-1':
                alist.append([at1, at2])
    all_atom = []
    for i in alist:
        at1, at2 = i[0],i[1]
        cmd.distance('res' + at1+'_'+at2, 'id ' + at1, 'id '+ at2)
        #cmd.hide('labels')
        cmd.label('id ' + at1, 'name')
        cmd.label('id ' + at2, 'name')
        all_atom.append(at1)
        all_atom.append(at2)
    all_atom = set(all_atom)
    selection = '+'.join(all_atom)
    cmd.color('white','res*')
    cmd.select('NOE_atoms','id '+selection)
    cmd.set('sphere_scale','0.2')
    cmd.show('sphere','id '+selection)
    cmd.set('dash_gap', 0.05)
    cmd.do("orient")
    cmd.set('movie_delay', 1500)
