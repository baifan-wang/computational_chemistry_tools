#!/bin/bash/env python3
__author__='Baifan Wang'
"""A simple script to compute the md5 and sha256 for input files.
Usage:
python python_md5_sha256.py file.
"""
import hashlib
import sys
def md5sum(file, blocksize=65536):
    hash = hashlib.md5()
    with open(file, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()
def sha256sum(file, blocksize=65536):
    hash = hashlib.sha256()
    with open(file, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

file = sys.argv[1]
md5 = md5sum(file)
sha256 = sha256sum(file)
print("The MD5SUMS for '%s' is: %s" %(file, md5))
print("The SHA256SUMS for '%s' is: %s" %(file,sha256))