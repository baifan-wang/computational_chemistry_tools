# computational_chemistry_tools
Some scripts for computationla chmeitry.
## [Amber](https://github.com/baifan-wang/computational_chemistry_tools/tree/master/Amber): scripts relate with [Amber Molecular Dynamics simulation software](http://ambermd.org/).

## [PDB](https://github.com/baifan-wang/computational_chemistry_tools/tree/master/PDB): scripts relate with [RCSB PDB file](http://www.rcsb.org/pdb/home/home.do).

## [gaussian](https://github.com/baifan-wang/computational_chemistry_tools/tree/master/gaussian): scripts to help process [gaussian](http://gaussian.com/) results log file.

## [autodock_analysis.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/autodock_analysis.py): A script to auto process, plot and recluster the dlg file generated by [Autodock](http://autodock.scripps.edu/).    
require: numpy, matplotlib
Usage:
```python
usage: python autodock_analysis.py [-h] [-i I] [-p] [-o O] [-plot]
                            [-recluster [RECLUSTER [RECLUSTER ...]]] [-replot]
'''optional arguments:
  -h, --help        show this help message and exit
  -i I              the input dlg file.
  -p                print the summary results in dlg.
  -o O              the output file, coordinates generated in docking process will also be written.
                        
  -plot             plot the 'number in cluster' vs 'lowest of cluster'.
  -recluster [RECLUSTER [RECLUSTER ...]]
                    recluster the result based on the input rms value. User should provide rmsd cutoff and a new filename.
                    eg: -recluster 4.0 xxx_recluster
  -replot           plot the 'number in cluster' vs 'lowest of cluster' after recluster.'''
```
The recluster algorithm is as follow:    
In the beginning the lowest energy conformation among all of the conformation will be used as the reference for the first cluster. The RMSD values of the remaining conformations with respect to reference will be computed. The conformations with RMSD values less than RMS cutoff will be grouped into first cluster. Then the reference will be the lowest energy conformation in the remaining conformations and process continue until all of the conformations are clustered. This process will generate new pdbs, lowest energy pdbs, rmsd_dict and cluster_data.    

## [g4_cation.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/g4_cation.py): Add cation to the center of 2 G-quartets. 
Using the average coordinates of O6 atom of guanine base as the coordinates of cations. Deafult cation is K+.
Usage: 
```python
python g_cation.py xxx.pdb  residue serial numbers in 1st G-quartet  2nd G-quaret ...
```
eg: python g_cation.py xxx.pdb 1,2,3,4  5,6,7,8  9,10,11,12    
in which the 1,2,3,4 are the residue serial numbers in 1st G-quartet. The cations will be added to the center of G-quartet 1-2-3-4 and 5-6-7-8 as well as the center of G-quartet 5-6-7-8 and 9-10-11-12

## [py_md5_sha256.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/py_md5_sha256.py): a simple python t compute the MD5 and SHA256 of a file.
Usage:
```python py_md5_sha256.py xxx.file
```

## [terminal_plot.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/terminal_plot.py): Python script for text-based plotting data in terminal, useful for ssh login. 

Sometimes people can only connect to remote server via ssh. To check the data generated on the remote server, one has to download these data. terminal_plot can directly display these data on the terminal to check whether is necessary to download these for further analysis.

Usage:     
```python    
python terminal_plot.py data.dat data_column 
```   
in which "data_column" specify which column data to plot(normally the first column (column 0) is used as x values, the second column (column 1) is the first y values).
![image](https://raw.githubusercontent.com/baifan-wang/computational_chemistry_tools/master/image/terminal_plot.png)
