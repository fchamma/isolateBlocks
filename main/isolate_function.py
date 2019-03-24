import csv

class block:
# block objects hold field names and can store data
    def __init__(self, list):
        self.name = list[0]
        try:
            self.len = list.index('')
        except:
            self.len = len(list)
        self.fields = ['BlockIdentifier', 'UniqueID'] + list[1:self.len]
        self.data = []

def parse_metadata(layout, delim=','):
# reads layout (metadata) file
# returns list of block objects
    blocks = list()
    with open(layout) as f:
        reader = csv.reader(f, delimiter=delim)
        for row in reader:
            blocks.append(block(row))
    return(blocks)

def get_last(list):
# get index for last non-empty element in a list
  for i, e in enumerate(reversed(list)):
    if e is not '':
      return len(list) - i - 1
  return -1

def parse_inputString(path, blocks, delim=',', idPos=2, idBlock=1):
# reads main file to isolate blocks from
# writes each block to a csv file
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
                    raise Exception('Error, line %d column %d: Invalid block name or wrong input string format' % (row_counter+1, i+1))
    return(blocks)

def write_block(block, path):
    ## add check for invalid extension
    if path[-1] == '/':
        filename = path + block.name + '.csv'
    else:
        filename = path + '/' + block.name + '.csv'
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(block.data)
    writeFile.close()
