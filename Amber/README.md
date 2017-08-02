## [makePLANAR_RST.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/Amber/makePLANAR_RST.py): Generate the planarity restraint for the input base pair to be used in Amber NMR calculation.    
Usage: 
```python
python makePLANAR_RST.py -i input_file -o output_file -res basepairs
python makePLANAR_RST.py -i wc.txt -o wc.dist      #read base pair definitation from wc.txt and output restraint to wc.dist
python makePLANAR_RST.py -res A 1 T 2 -o wc.dist   #read base pair definitation from input and output restraint to wc.dist
python makePLANAR_RST.py -res A 1 T 2 -i wc.txt -o wc.dist   #read base pair definitation from both input and wc.txt output restraint to wc.dist
python makePLANAR_RST.py -res A 1 T 2  #direct print the output 
```
-res: input residues type for base pair, eg: G 1 G 2 G 3    
input_file: base pair planarity definition file, eg:    
T 1 A 2    
T 2 A 3    
...

## [remd_rate_calculator.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/Amber/remd_rate_calculator.py): calculate the exchange in the Replica exchange molecular dynamics simulation (REMD).
usage: 
```python
python rem_rate_calculator.py rem.log
```

## [amd_generate.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/Amber/remd_rate_calculator.py): create sander/pmemd input file for Accelerated Molecular Dynamics(AMD).
usage:
```python
python amd_generate.py md.output residue_number atom_number simulation_time(in ns)
```
See the following for detail:    
Running aMD requires the definition of few parameters. AMD parameters are determined based on previous knowledge of the system, which is easily acquirable by a short regular MD simulation, from which the average values of the potential and torsion energy can be estimated. From there, a given amount of energy per degree of freedom is added those values, in the form of multiples of alpha, setting the values of Ep and Ed to be used. The following example should help clarify this procedure.    
Average Dihedral : 611.5376 (based on MD simulations)    
Average EPtot : -53155.3104 (based on MD simulations)    
total ATOMS=16950    
protein residues=64    
For the dihedral potential:    
Approximate energy contribution per degree of freedom.    
3.5*64= 224 The value of 3.5 kcal/mol/residue seems to work well    
alphaD = (1/5)*224 = 45 The value of .2 seems to work well    
EthreshD = 224+611 = 835    
For the total potential    
alphaP = 16950*(1/5)=3390    
For a lower boost you can also use a value between 0.15-0.19 instead of 0.20 (0.16 works well)    
EthreshP = -53155.3104 + 3390 = -49765.3104    
With these parameters, the aMD parameters in the input file should then be set to    
iamd=3,EthreshD=835,alphaD=45,EthreshP=-49765,alphaP=3390,    
For a higher acceleration it is common to simply add to Eb(dih) multiples of alpha. In this example, iamd=3,EthreshD=880,alphaD=45,EthreshP=-49765,alphaP=3390,    
Two levels higher would be then defined by:    
iamd=3,EthreshD=925,alphaD=45,EthreshP=-49765    
