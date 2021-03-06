## [pdb_downloader.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/PDB/pdb_downloader.py): download a PDB file form RCSB PDB database.
usage:
```python
python pdb_downloader.py PDBID
```
in which PDBID is a four letter number+letter, such as: 5LIG

## [pdb_re_bfactor.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/PDB/pdb_re_bfactor.py): replace the bfactor column of a pdb file from a data file.      
If a data file is supplied, it reads atom number/b-factor pairs and places the values in the b-factor column of a pdb file. Test on Amber generate pdb and B-factor file.
usage:  
```python
python pdb_re_bfactor.py xxx.pdb  bfactor.file
```

## [pdbtoseq.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/PDB/pdbtoseq.py): A script data to extract sequence from pdb and return sequence information FASTA format.
It will try to read SEQRES entries; otherwise it will extract sequence information in Atom section.
Usage:  
```python
python pdbtoseq.py xxx.pdb
```
## [splitnmr.py](https://github.com/baifan-wang/computational_chemistry_tools/blob/master/PDB/splitnmr.py): A script to split each model of pdb into separate pdb files.
Usage:  
```python
python splitnmr.py xxx.pdb
```
