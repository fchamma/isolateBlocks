import csv, sys, os

# define block objects, which hold field names and can store data
class block:
    def __init__(self, list):
        self.name = list[0]
        try:
            self.len = list.index('')
        except:
            self.len = len(list)
        self.fields = ['BlockIdentifier', 'UniqueID'] + list[1:self.len]
        self.data = [self.fields]
        self.count = 0
    def count_occurrences(self, file):
        with open(file, 'r') as f:
            reader = f.read()
            self.count = reader.count(self.name)

# read layout (metadata) file and returns list of block objects
def parse_metadata(layout, delim=',', idBlock=1, idPos=2):
    blocks = list()
    row_counter = 0
    with open(layout) as f:
        reader = csv.reader(f, delimiter=delim)
        for row in reader:
            row_counter += 1
            blocks.append(block(row))
            if idBlock == row_counter:
                del blocks[-1].fields[idPos]
    return(blocks)

# get index for last non-empty element in a list
def get_last(list):
  for i, e in enumerate(reversed(list)):
    if e is not '':
      return len(list) - i - 1
  return -1

# read main file to isolate blocks and return updated block objects
def parse_inputString(path, blocks, labels, delim=',', idPos=2, idBlock=1, verbose = False):
    names = []
    for b in blocks:
        names.append(b.name)
    with open(path) as f:
        reader = csv.reader(f, delimiter=delim)
        row_counter = 0
        for row in reader:
            row_counter += 1
            UniqueID = row[idPos-1]
            del row[idPos-1]
            n_fields = get_last(row)
            i = 0
            while i < n_fields:
                if row[i] == names[idBlock-1]:
                    block = blocks[idBlock-1]
                    block.data.append([row[i]] + [UniqueID] + row[i+1:i+block.len-1])
                    i += block.len-1
                elif row[i] in names:
                    block = next((x for x in blocks if x.name == row[i]), None)
                    block.data.append([row[i]] + [UniqueID] + row[i+1:i+block.len])
                    i += block.len
                else:
                    if verbose:
                        raise Exception(labels['err9'] % (row_counter, i+1))
                    else:
                        print(labels['err9'] % (row_counter, i+1))
                        sys.exit()
    return(blocks)

# write a given block to the given path
def write_block(block, path, labels, overwrite = False):
    if path[-1] == '/':
        filename = path + block.name + '.csv'
    else:
        filename = path + '/' + block.name + '.csv'
    # checking before overwriting file
    if os.path.isfile(filename) and overwrite == False:
        user_input = input(labels['owPrompt'] % block.name)
        if user_input == 'y' or user_input == 'Y':
            print(labels['statusWritingFile'] % block.name, end="", flush=True)
            with open(filename, 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(block.data)
            writeFile.close()
            print(labels['statusWritingSuccess'])
            return('Success')
        else:
            print(labels['owDenied'])
            return('Skipped')
    else:
        print(labels['statusWritingFile'] % block.name, end="", flush=True)
        with open(filename, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(block.data)
        writeFile.close()
        print(labels['statusWritingSuccess'])
        return('Success')

# check if number of occurrences of a block name matches number of rows in output file
def check_occurrences(blocks, path, labels):
    msg = labels['checkOccInit']
    check = False
    for b in blocks:
        b.count_occurrences(path)
        if b.count != len(b.data)-1:
            check = True
            msg += '    ' + b.name + ': Input string has ' + str(b.count) +\
            ' occurrences; Output file has ' + str(len(b.data)-1) + ' rows \n'
    msg += labels['checkOccFinal']
    msg += labels['isolateSuccess']
    if check == True:
        print(msg)
    # else:
    #     print(labels['isolateSuccess'])
