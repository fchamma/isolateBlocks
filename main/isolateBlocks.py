import argparse
import os
import sys
from isolate_function import *

# Defining help messages
helpDescription = 'Isolates given input string file into individual blocks, based on a layout file'
helpMsgFile = 'Path of character delimited file to be isolated'
helpMsgLayout = 'Path of character delimited metadata file. Use one block layout per line, with field names separated by delimiters'
helpMsgFileDelim = "Character delimiter for main file. Defaults to ','. Pass argument WITHOUT quotes"
helpMsgLayoutDelim = 'd'
helpMsgIdPos = 'e'
helpMsgIdBlock = 'f'
helpMsgDest = 'g'
helpMsgVerb = 'Increase output verbosity'

parser = argparse.ArgumentParser(helpDescription)
parser.add_argument('file', help = helpMsgFile)
parser.add_argument('layout', help = helpMsgLayout)
parser.add_argument('-d', '--destination', default = './', help = helpMsgDest)
parser.add_argument('-fd', '--fileDelimiter', help = helpMsgFileDelim, metavar='N', default = ",")
parser.add_argument('-ld', '--layoutDelimiter', help = helpMsgLayoutDelim, metavar='N', default = ",")
parser.add_argument('-idp', '--idPosition', help = helpMsgIdPos, type = int, metavar='N', default = 2)
parser.add_argument('-idb', '--idBlock', help = helpMsgIdBlock, type = int, metavar='N', default = 1)
parser.add_argument("-v", "--verbose", action="store_true", help = helpMsgVerb)
args = parser.parse_args()

def validate_args(args):
    if args.verbose == True:
        if not os.path.isfile(args.file):
            raise Exception('Input path does not exist or is not a file')
        if not os.path.isfile(args.layout):
            raise Exception('Layout (metadata) path does not exist or is not a file')
    else:
        if not os.path.isfile(args.file):
            print('\n ERROR: Input path does not exist or is not a file')
            sys.exit()
        if not os.path.isfile(args.layout):
            print('\n ERROR: Layout path does not exist or is not a file')
            sys.exit()



def main():
    blocks = parse_metadata(args.layout, args.layoutDelimiter)
    blocks = parse_inputString(args.file, blocks, args.fileDelimiter, args.idPosition, args.idBlock)
    for b in blocks:
        write_block(b, args.destination)

if __name__ == '__main__':
    validate_args(args)
    main()  # Or whatever function produces output
