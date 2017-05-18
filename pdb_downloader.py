#!/usr/bin/env python3

"""
download a PDB file from the RCSB database.
usage: python pdb_downloader.py pdbid
"""
__auther__ = 'Baifan Wang'

import urllib.request
from urllib.error import HTTPError
import sys

def downloader(pdbid):
    pdbid = pdbid.lower()
    base_url = 'http://www.rcsb.org/pdb/files/'
    pdb_url = base_url + pdbid + '.pdb'
    try:
        urllib.request.urlretrieve(pdb_url, pdbid+'.pdb')
    except HTTPError as e:
        print('Unable to downloadpdb: (%s) %s' %(e.code, e.msg))
        raise

if __name__ == '__main__':
    if len(sys.argv) !=2:
        print('Usage python pdb_downloader.py pdbid')
    pdb_id = sys.argv[1]
    downloader(pdb_id)
    print('Successfully download the pdb: %s.pdb' %pdb_id)
