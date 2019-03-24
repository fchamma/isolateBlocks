from isolate_function import *

layout = "C:/Users/FelipeCiottiChamma/Desktop/aux_projects/isolateBlocks/data/metadata1.csv"
path = "C:/Users/FelipeCiottiChamma/Desktop/aux_projects/isolateBlocks/data/testData.csv"
outpath = "C:/Users/FelipeCiottiChamma/Desktop/aux_projects/isolateBlocks/data"
a = parse_metadata(layout)
b = parse_inputString(path, a)

# print(b)
for e in b:
    print (e.data)

write_block(b[0], outpath)
