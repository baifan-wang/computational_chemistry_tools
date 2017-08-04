
[make_restraint.sh]( https://github.com/baifan-wang/computational_chemistry_tools/blob/master/NMR_structure_calculation/make_restraint.sh): script to make restraint file. The restraint including NOE and hydrogen bond distance restraints, torsion angle restraint, planarity restraints (optional) and chirality restraint. The final restraint file created by this script is ‘RST.dist’. Usage:    
bash make_restraint.sh    
Assuming you already have the following files:    
* 1.pdb: pdb file for you initial structure. If you have different file name, change it in script.    
* noe.8col : NOE 8 column restraint file     
* hbond.8col: hydrogen bond 8 column restraint file     
* torsion.5col: torsion 5 column restraint file    
* planarity.dist: planarity restraint file (optional, you need to manually edit or create using [makePLANAR_RST.py](https://github.com/baifan-wang/computational_chemistry_tools/tree/master/Amber)    
* map_added.DG-AMBER: MAP file for creating NOE and hydrogen bond restraint    
* tordef.lib: library file for creating torsion restraint    
The ‘map_added.DG-AMBER’ and ‘tordef.lib’ can be found in this repositoriy, as well as examples for the ‘noe.8col’, ‘hbond.8col’, ‘torsion.5col’ and ‘planarity.dist’.    
