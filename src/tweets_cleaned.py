#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python can normally handle large files when reading because
>	with open('file.txt') as f:
>		for line in f:
>			print line
automatically buffers (see the StackOver slow discussion at
http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python).

This module calls the function _clean_string from utils, which returns a list whether a 
tweet had unicode(False), Or has no unicode/escape characters(True)

The input is read from a file, as specified in run.sh first command. 

"""

import sys
import json
from utils import _clean_string


def main(argv):

    num_unicode = 0
    inp_file, out_file = argv

    out_put = open(out_file,'w')

    with open(inp_file) as input_file:
        for line in input_file:
            line = line.rstrip()
            line_json = json.loads(line)
            try:
                clean, cleaned_line = _clean_string(line_json["text"])
                if not clean:
                    num_unicode += 1
                out_put.write(cleaned_line + " (timestamp: {0})".format(line_json["created_at"]) + "\n")
            except:
                #this except block is here to handle the following sample limit lines
                # {"limit":{"track":19,"timestamp_ms":"1446218985758"}}
                pass
        
    out_put.write("\n {0} tweets contained unicode.".format(num_unicode))
    out_put.close()
    input_file.close()
    
if __name__ == "__main__":
   main(sys.argv[1:])
