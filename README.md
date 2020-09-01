Readme

Scyther takes a varexp file, and a tag filter and then removes all the filtered tags 
from the varexp file. It does NOT modify the original file. 

Instead, Scyther creates two files, a varexp file without the filtered tags
and a file that only contains the filtered tags

Open a powershell window. and cd to this directory.

Then type in the following line

python .\Scyther.py -filePath [FILEPATH] -filter [tag format to extract]

Example:  To extract all BIO tags from a Varexp file

python .\Scyther.py -filePath .\Varexp.txt -filter BIO 

A few things to note: 

- Scyther recognizes a tag in dot notation, so in the form of "XXXXX.YYYYY.ZZZZZ"
- The filter flag can accept regular expressions as well. Don't worry too much if you don't know what this is