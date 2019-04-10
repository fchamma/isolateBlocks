from __future__ import print_function
import csv, sys, os
from base import *

# read blocks to concatenate
def parse_inputBlocks(input_folder, delim=',', idPos=2):
    input_blocks = os.listdir(input_folder)
    blocks = list()
    if input_folder[-1] != '/':
        input_folder += '/'
    for file in input_blocks:
        with open(input_folder+file, 'r') as f:
            reader = csv.reader(f, delimiter=delim)
            # initiating block instance with header row
            blocks.append(block(next(reader), non_id=2))
            blocks[-1].name = file.split('.')[0]
            # sorting blocks upon parsing to help with upcoming concatenation
            sortedReader = sorted(reader, key=lambda row: row[idPos-1])
            curr_id = None
            for row in sortedReader:
                if row[idPos-1] == curr_id:
                    blocks[-1].data[-1] += row[:idPos-1]
                    blocks[-1].data[-1] += row[idPos:]
                else:
                    curr_id = row[idPos-1]
                    blocks[-1].data.append(row)
    return(blocks)

# sort list of blocks based on desired order passed on cmd input
def sort_block_write_order(blocks, write_order):
    write_order = [i.lower() for i in write_order]
    for b in blocks:
        if b.name.lower() in write_order:
            b.get_order(write_order.index(b.name.lower()))
        else:
            b.order = 999
    return(sorted(blocks, key=lambda x: x.order))

# output is further populated with all other blocks
def populate_output(blocks, idPos=2):
    # initiate output with header data, which must have all IDs
    output = blocks[0].data[1:]
    for b in blocks[1:]: # iterate all other blocks
        i = 0
        for row in b.data[1:]:
            # matching block ID and output ID line by line (IDs are sorted)
            for out in output[i:]:
                i += 1 # counter to skip past used ids in outfile iteration
                if row[idPos-1] == out[idPos-1]:
                    out += row[:idPos-1]
                    out += row[idPos:]
                    break
    return(output)

# write output to file
def write_output_py2(output, filename, labels, overwrite = False):
    # checking before overwriting file
    if os.path.isfile(filename) and overwrite == False:
        user_input = raw_input(labels['owPrompt'] % filename.split('/')[-1])
        if user_input == 'y' or user_input == 'Y':
            print(labels['statusWritingFileConcat'], end="")
            with open(filename, 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(output)
            writeFile.close()
            print(labels['statusWritingSuccess'])
            return('Success')
        else:
            print(labels['owDenied'])
            return('Skipped')
    else:
        print(labels['statusWritingFileConcat'], end="")
        with open(filename, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(output)
        writeFile.close()
        print(labels['statusWritingSuccess'])
        return('Success')

# write output to file
def write_output_py3(output, filename, labels, overwrite = False):
    # checking before overwriting file
    if os.path.isfile(filename) and overwrite == False:
        user_input = input(labels['owPrompt'] % filename.split('/')[-1])
        if user_input == 'y' or user_input == 'Y':
            print(labels['statusWritingFileConcat'], end="")
            with open(filename, 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(output)
            writeFile.close()
            print(labels['statusWritingSuccess'])
            return('Success')
        else:
            print(labels['owDenied'])
            return('Skipped')
    else:
        print(labels['statusWritingFileConcat'], end="")
        with open(filename, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(output)
        writeFile.close()
        print(labels['statusWritingSuccess'])
        return('Success')
