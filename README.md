### Parsing delimited files with varying number of fields
This utility parses delimited files where each row contains a custom number of fields, by identifying "blocks" of fields based on a layout (metadata) file.

The utility can take a single delimited file and write its blocks into several csv files (isolate.py) function or the other way around, reading in the isolated block files and joining them into a single csv.

#### isolate.py
Isolates data blocks from a delimited text file based on a given layout file. The layout (or metadata) file should have one row per existing block, with each block field separated by the delimiter.

E.g. Input file:\n
"""\n
Header,1,19910131,Acc,bankX,active,Acc,bankY,inactive,Phone,home,123456,no\n
Header,2,19690315,Acc,bankZ,inactive,Phone,home,54321,yes,Phone,mobile,9876,no\n
Header,3,19491121\n
"""

E.g. Layout file:\n
"""\n
Header,UniqueID,DOB\n
Acc,Bank Name,Status\n
Phone,Type,Number,Contact\n
"""

Passing the input and layout files above into the isolate.py function will write 3 files to the destination directory. File names are taken from the block names (1st position of layout file). First position is reserved for block identifier (name) and second position is reserved for UniqueID:

1) Header.csv:\n
"""\n
BlocksIdentifier,UniqueID,DOB\n
Header,1,19910131\n
Header,2,19690315\n
Header,3,19491121\n
"""

2) Acc.csv:\n
"""\n
BlocksIdentifier,UniqueID,Bank Name,Status\n
Acc,1,bankX,active\n
Acc,1,bankY,inactive\n
Acc,2,bankZ,inactive\n
"""

3) Phone.csv:\n
"""\n
BlocksIdentifier,UniqueID,Type,Number,Contact\n
Phone,1,home,123456,no\n
Phone,2,home,54321,yes\n
Phone,2,mobile,9876,no\n
"""

User can also define the following optional command line arguments:
-d str, --destination str
                      Destination folder where blocks will be written to.
                      Defaults to the working directory
-fd str, --fileDelimiter str
                      Character delimiter for main file. Defaults to ','.
                      Pass argument WITHOUT quotes
-ld str, --layoutDelimiter str
                      Character delimiter for main file. Defaults to ','.
                      Pass argument WITHOUT quotes
-idp int, --idPosition int
                      Position of record identifier (UniqueID) within each
                      input string row. Defaults to '2' (second position)
-idb int, --idBlock int
                      Position of block with record identifier (UniqueID)
                      within layout file. Defaults to '1' (first block),
                      usually the header
-ow, --overwrite      Flag to silently overwrite output file for each block,
                      if they already exist. If omitted, user will be
                      prompted before any overwriting
-v, --verbose         Increase output verbosity (mostly for code debugging)
