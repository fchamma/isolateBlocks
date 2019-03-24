import argparse, os, sys
from isolate_function import *

# Retrieving help and error messages, stored as dictionaries in txt files
script_dir = os.path.dirname(__file__)
labelsPath = os.path.join(script_dir, 'labels.txt')
with open(labelsPath) as f:
    labels = eval(f.read())

# Parsing command line arguments
parser = argparse.ArgumentParser(labels['helpDescription'])
parser.add_argument('file', help = labels['helpMsgFile'])
parser.add_argument('layout', help = labels['helpMsgLayout'])
parser.add_argument('-d', '--destination', default = './', help = labels['helpMsgDest'], metavar='str')
parser.add_argument('-fd', '--fileDelimiter', default = ",", help = labels['helpMsgFileDelim'], metavar='str')
parser.add_argument('-ld', '--layoutDelimiter', default = ",", help = labels['helpMsgLayoutDelim'], metavar='str')
parser.add_argument('-idp', '--idPosition', default = 2, help = labels['helpMsgIdPos'], type = int, metavar='int')
parser.add_argument('-idb', '--idBlock', default = 1, help = labels['helpMsgIdBlock'], type = int, metavar='int')
parser.add_argument("-v", "--verbose", action="store_true", help = labels['helpMsgVerb'])
args = parser.parse_args()

# Basic checks before running the main functions to save processing time
def validate_args(args):
    if args.verbose == True:
        if not os.path.isfile(args.file):
            raise Exception(labels['err1'])
        if not os.path.isfile(args.layout):
            raise Exception(labels['err2'])
        if not os.path.exists(args.destination):
            raise Exception(labels['err3'])
    else:
        if not os.path.isfile(args.file):
            print('\n ERROR: ', labels['err1'])
            sys.exit()
        if not os.path.isfile(args.layout):
            print('\n ERROR: ', labels['err2'])
            sys.exit()
        if not os.path.exists(args.destination):
            print('\n ERROR: ', labels['err3'])
            sys.exit()


# Function to group necessary functions for command line run
def main():
    blocks = parse_metadata(args.layout, args.layoutDelimiter)
    blocks = parse_inputString(args.file, blocks, args.fileDelimiter, args.idPosition, args.idBlock)
    for b in blocks:
        write_block(b, args.destination)
    check_occurrences(blocks, args.file, labels)

if __name__ == '__main__':
    validate_args(args)
    main()
