from __future__ import print_function
import argparse, os, json, sys, time
from parse_args_isolate import *
from isolate_dependencies import *
from base import *

# Retrieving help and error messages, stored as dictionaries in txt files
script_dir = os.path.dirname(__file__)
labelsPath = os.path.join(script_dir, 'labels.txt')
with open(labelsPath) as f:
    labels = json.loads(f.read())
f.close()

# Parsing command line arguments
parser = argparse.ArgumentParser(labels['helpDescription'])
parser.add_argument('file', help = labels['helpMsgFile'])
parser.add_argument('layout', help = labels['helpMsgLayout'])
parser.add_argument('-d', '--destination', default = './', help = labels['helpMsgDest'], metavar='str')
parser.add_argument('-fd', '--fileDelimiter', default = ",", help = labels['helpMsgFileDelim'], metavar='str')
parser.add_argument('-ld', '--layoutDelimiter', default = ",", help = labels['helpMsgLayoutDelim'], metavar='str')
parser.add_argument('-idp', '--idPosition', default = 2, help = labels['helpMsgIdPos'], type = int, metavar='int')
parser.add_argument('-idb', '--idBlock', default = 1, help = labels['helpMsgIdBlock'], type = int, metavar='int')
parser.add_argument('-ow', '--overwrite', action="store_true", help = labels['helpMsgOverwrite'])
parser.add_argument('-cc', '--countCheck', action="store_true", help = labels['helpMsgCountCheck'])
parser.add_argument("-v", "--verbose", action="store_true", help = labels['helpMsgVerb'])
args = parser.parse_args()

# Function to group necessary functions for command line run
def main():
    print(labels['statusIsolationStarted'])
    blocks = parse_metadata(args.layout, args.layoutDelimiter, args.idBlock, args.idPosition)
    blocks = parse_inputString(args.file, blocks, labels, args.fileDelimiter, args.idPosition, args.idBlock, args.verbose)
    success = []
    skipped = []
    for b in blocks:
        if sys.version_info[0] < 3:
            res = write_block_py2(b, args.destination, labels, args.overwrite)
        else:
            res = write_block_py3(b, args.destination, labels, args.overwrite)
        if res == 'Success':
            success.append(b.name)
        else:
            skipped.append(b.name)
    if args.countCheck:
        check_occurrences(blocks, args.file, labels)
    if len(skipped) == 0:
        print(labels['isolateSuccessAll'])
    elif len(success) == 0:
        print(labels['isolateSkippedAll'])
    else:
        print(labels['isolateSuccess'] % success)
        print(labels['isolateSkipped'] % skipped)

if __name__ == '__main__':
    start_time = time.time()
    validate_args(args, labels)
    main()
    print(labels['elapsedTime'] % round(time.time() - start_time, 2))
