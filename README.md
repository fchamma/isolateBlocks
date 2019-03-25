# Isolate Blocks Utility
## Parsing delimited files with varying number of fields
This utility parses delimited files where each row contains a custom number of fields, by identifying "blocks" of fields based on a layout (metadata) file.

The function **isolate.py** isolates data blocks from a delimited text file based on a given layout file. The layout (or metadata) file should have one row per existing block, with each
block field separated by the delimiter.

#### Example
```console
cat ./test_data/input_1.csv # (input file)
```
"""  
Header,1,19910131,Acc,bankX,active,Acc,bankY,inactive,Phone,home,123456,no  
Header,2,19690315,Acc,bankZ,inactive,Phone,home,54321,yes,Phone,mobile,9876,no  
Header,3,19491121  
"""

```console
cat ./test_data/layout_1.csv # (layout file)
```
"""  
Header,UniqueID,DOB  
Acc,Bank Name,Status  
Phone,Type,Number,Contact  
"""

Passing the input and layout files above into the isolate.py function will write 3 files to the destination directory. File names are taken from the block names (1st position of layout file). First position is reserved for block identifier (name) and second position is reserved for UniqueID:

```console
python main/isolate.py test_data/input_1.csv test_data/layout_1.csv -d test_data/output
```

1) Header.csv:  
"""  
BlocksIdentifier,UniqueID,DOB  
Header,1,19910131  
Header,2,19690315  
Header,3,19491121  
"""

2) Acc.csv:  
"""  
BlocksIdentifier,UniqueID,Bank Name,Status  
Acc,1,bankX,active  
Acc,1,bankY,inactive  
Acc,2,bankZ,inactive  
"""

3) Phone.csv:  
"""  
BlocksIdentifier,UniqueID,Type,Number,Contact  
Phone,1,home,123456,no  
Phone,2,home,54321,yes  
Phone,2,mobile,9876,no  
"""  

The optional -d (--destination) argument used above defines the folder where the blocks will be written to. If not specified, files will be written to working directory.

If output files already exist, user will be prompted to overwrite them or not, individually. Alternatively, the optional flag -ow (--overwrite) can be passed to bypass the prompt:

```console
python main/isolate.py test_data/input_1.csv test_data/layout_1.csv -ow
```

For more info on function usage and arguments please refer to help contents. Use command:
```console
python isolate.py -h
```
