from __future__ import print_function
import csv, sys, os, time, json
from itertools import islice
from base import *
from isolate_dependencies import *
t = time.time()
labelsPath = "./main/labels.txt"
with open(labelsPath) as f:
    labels = json.loads(f.read())
f.close()

# arguments from user to be parsed in main()
exampleFile = '1'
infile = "./test_data/input_" + exampleFile + ".csv"
layfile = "./test_data/layout_" + exampleFile + ".csv"
outfolder = "./test_data/output_" + exampleFile
delim=','
idPos=2
idBlock=1

# starting blocks
blocks = parse_metadata(layfile, delim, idBlock, idPos)
for b in blocks:
    print(b.name, ": ", b.data)

# testing sort function
blocks = parse_inputString(infile, blocks, labels, delim, idPos, idBlock)

for b in blocks:
    write_block_py2(b, outfolder, labels)

print('time elapsed:', time.time() - t)
