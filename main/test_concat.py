from __future__ import print_function
import csv, sys, os, time, json
from itertools import islice
from base import *
from concatenate_dependencies import *
t = time.time()
labelsPath = "./main/labels.txt"
with open(labelsPath) as f:
    labels = json.loads(f.read())
f.close()

# arguments from user to be parsed in main()
exampleFile = '1'
input_folder = "./test_data/input_" + exampleFile
comparefile = "./test_data/input_" + exampleFile + ".csv"
outfile = "./test_data/output_" + exampleFile + ".csv"
delim=','
idPos=2
# write_order = ['header']
write_order = ['Header', 'Acc', 'Phone']

# starting blocks
blocks = parse_inputBlocks(input_folder, delim, idPos)

# testing sort function
blocks = sort_block_write_order(blocks, write_order)
# for b in blocks:
#     print(b.data)

# populating output
output = populate_output(blocks)


# writing output to disk
# print(output)
if sys.version_info[0] < 3:
    res = write_output_py2(output, outfile, labels, overwrite = True)
else:
    res = write_output_py3(output, outfile, labels, overwrite = True)
print(res)

# comparing expected result
oList = []
cList = []

with open(outfile, 'r') as outFile:
    outWriter = csv.reader(outFile)
    for row in outWriter:
        oList.append(row)
outFile.close()

with open(comparefile, 'r') as compareFile:
    compareWriter = csv.reader(compareFile)
    compareWriter = sorted(compareWriter, key=lambda row: row[idPos-1])
    for row in compareWriter:
        cList.append(row)
compareFile.close()
# print(oList)
# print(cList)
compare =  [x==y for (x,y) in zip(oList, cList)]
print(oList[:10])
print(cList[:10])
print(sum(compare), len(compare))

print('time elapsed:', time.time() - t)
