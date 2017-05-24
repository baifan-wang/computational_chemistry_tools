[makePLANAR_RST.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/Amber/makePLANAR_RST.py): Generate the planarity restraint for the input base pair to be used in Amber calculation.    
Usage: python makePLANAR_RST.py -i base pair planarity definition file        
                                -o output the planarity restraints file    
				-res  input residues type for base pair, eg: G 1 G 2 G 3    
example for "base pair planarity definition file":    
T 1 A 2    
T 2 A 3    
...
