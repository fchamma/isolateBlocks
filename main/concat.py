from __future__ import print_function
import argparse, os, json, sys, time
from parse_args_concatenate import *
from concatenate_dependencies import *
from base import *

# Retrieving help and error messages, stored as dictionaries in txt files
script_dir = os.path.dirname(__file__)
labelsPath = os.path.join(script_dir, 'labels.txt')
with open(labelsPath) as f:
    labels = json.loads(f.read())
f.close()

# Parsing command line arguments
parser = argparse.ArgumentParser(labels['helpDescription'])
parser.add_argument('inputFolder', help = labels['helpMsgInputFolder'])
parser.add_argument('outfile', help = labels['helpMsgOutfile'])
parser.add_argument('header', nargs='*', default = 'header', help = labels['helpMsgHeader'])
parser.add_argument('-e', '--extension', default = 'csv', help = labels['helpMsgExtension'], metavar='str')
parser.add_argument('-fd', '--fileDelimiter', default = ',', help = labels['helpMsgFileDelim'], metavar='str')
parser.add_argument('-idp', '--idPosition', default = 2, help = labels['helpMsgIdPos'], type = int, metavar='int')
parser.add_argument('-ow', '--overwrite', action='store_true', help = labels['helpMsgOverwrite'])
# parser.add_argument("-v", "--verbose", action="store_true", help = labels['helpMsgVerb'])
args = parser.parse_args()

# Function to group necessary functions for command line run
def main():
    print(labels['statusConcatenationStarted'])
    blocks = parse_inputBlocks(args.inputFolder, args.fileDelimiter, args.idPosition)
    blocks = sort_block_write_order(blocks, args.header)
    output = populate_output(blocks)
    if sys.version_info[0] < 3:
        try:
            res = write_output_py2(output, args.outfile, labels, args.overwrite)
        except:
            print(labels['statusConcatenationFailed'])
            sys.exit()
    else:
        try:
            res = write_output_py3(output, args.outfile, labels, args.overwrite)
        except:
            print(labels['statusConcatenationFailed'])
            sys.exit()
    if res == 'Success':
        print(labels['statusConcatenationSuccess'])

if __name__ == '__main__':
    start_time = time.time()
    # validate_args(args, labels)
    main()
    print(labels['elapsedTime'] % round(time.time() - start_time, 2))
