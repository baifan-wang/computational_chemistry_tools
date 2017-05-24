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
