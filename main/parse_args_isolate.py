from __future__ import print_function
import argparse, os, sys

# Check if integer is positive
def is_positive(n, threshold = 0):
    if n > threshold:
        return True
    else:
        return False

# Basic checks before running the main functions to save processing time
def validate_args(args, labels):
    if args.verbose:
        if not os.path.isfile(args.file):
            raise Exception(labels['err1'])
        if not os.path.isfile(args.layout):
            raise Exception(labels['err2'])
        if not os.path.exists(args.destination):
            raise Exception(labels['err3'])
        if not os.access(args.destination, os.W_OK):
            raise Exception(labels['err4'])
        if not is_positive(args.idPosition, threshold=1):
            raise Exception(labels['err5'])
        if not is_positive(args.idBlock):
            raise Exception(labels['err6'])
        if len(args.fileDelimiter) > 1:
            raise Exception(labels['err7'])
        if len(args.layoutDelimiter) > 1:
            raise Exception(labels['err8'])
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
        if not os.access(args.destination, os.W_OK):
            print('\n ERROR: ', labels['err4'])
            sys.exit()
        if not is_positive(args.idPosition, threshold=1):
            print('\n ERROR: ', labels['err5'])
            sys.exit()
        if not is_positive(args.idBlock):
            print('\n ERROR: ', labels['err6'])
            sys.exit()
        if len(args.fileDelimiter) > 1:
            print('\n ERROR: ', labels['err7'])
            sys.exit()
        if len(args.layoutDelimiter) > 1:
            print('\n ERROR: ', labels['err8'])
            sys.exit()
