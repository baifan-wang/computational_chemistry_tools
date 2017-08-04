This repository provides protocol and scripts for simulated annealing simulation for NMR structure calculation.    
## Create initial strcuture. 
Here the initial strucutre are created by 'leap' programm in amber. The 'leap.in' is a script containing the commands to load force field parameters, create initial structure, save files, etc. The current 'leap.in' is designed for the DNA molecule using the 'ff-nucleic-OL15' force field (see http://fch.upol.cz/ff_ol/downloads.php for detail). One can download these force field in this repository('ff-nucleic-OL15.frcmod' and 'ff-nucleic-OL15.lib') or from  http://fch.upol.cz/ff_ol/downloads.php.    
First you need to edit 'leap.in', input the sequence of your structure in {} in this line: "aaa = sequence {DG5 DG DG DG3}".    
Then use the following command to create amber topology and coordinate as well as pdb file:    
```bash
tleap -f leap.in
```
check if '1.top', '1.crd' and '1.pdb' are created. Check the '1.pdb' using Chimera or pymol.

## Minimization of initial structure.
The 'min.in' is the input parameter file for running minimization using sander or pmemd in amber.
Minimize your initial structure using the following command:
```bash
pmemd.cuda -O -i min.in -p 1.top -c 1.crd -r 1.rst -o min.out
```
Assuming you have the GPU-accelerated pmemd programm. Otherwise you can use 'sander', 'pememd', 'sander.MPI' or 'pmemd.MPI'.
This minimization will create the minimized coordinate '1.rst'. You can convert it into pdb file using:
```bash
ambpdb -p 1.top -c 1.rst >1.pdb
```

## Create restraints.
The NMR restraints file using in structure calculation are created by script: [make_restraint.sh]( https://github.com/baifan-wang/computational_chemistry_tools/blob/master/NMR_structure_calculation/make_restraint.sh). The restraints include NOE and hydrogen bond distance restraints, torsion angle restraint, planarity restraints (optional) and chirality restraints. The final restraint file created by this script is ‘RST.dist’. Usage:    
```bash
bash make_restraint.sh    
```
Assuming you already have the following files:    
* 1.pdb: pdb file for you initial structure. If you have different file name, change it in script.    
* noe.8col : NOE 8 column restraint file     
* hbond.8col: hydrogen bond 8 column restraint file     
* torsion.5col: torsion 5 column restraint file    
* planarity.dist: planarity restraint file (optional, you need to manually edit or create using [makePLANAR_RST.py](https://github.com/baifan-wang/computational_chemistry_tools/tree/master/Amber))    
* map_added.DG-AMBER: MAP file for creating NOE and hydrogen bond restraint    
* tordef.lib: library file for creating torsion restraint    
The ‘map_added.DG-AMBER’ and ‘tordef.lib’ can be found in this repositoriy, as well as examples for the ‘noe.8col’, ‘hbond.8col’, ‘torsion.5col’ and ‘planarity.dist’.    
