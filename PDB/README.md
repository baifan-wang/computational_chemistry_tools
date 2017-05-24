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
