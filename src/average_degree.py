#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

The input is read from a file, as specified in run.sh first command. 

Each of the line is iteratively parsed, cleaned, and hashtags are extracted. 

Graph is created/updated for each of hashtags. Edges created 60 secs. ago are deleted. 

"""

import sys
import json
import datetime
from dateutil import parser as dtparser
from utils import _clean_string, get_hashtag, calculate_avg_degree, update_or_build_graph, shuffle_graph


def main(argv):

    inp_file, out_file = argv
    
    graph = {}
    
    out_put = open(out_file,'w')
    
    with open(inp_file) as input_file:
        for line in input_file:
            line = line.rstrip()
            line_json = json.loads(line)
            try:
                created_at = dtparser.parse(line_json["created_at"])
                clean, cleaned_line = _clean_string(line_json['text'])
                hash_tags = get_hashtag(cleaned_line)
                if hash_tags:
                    graph = update_or_build_graph(graph, hash_tags, created_at)
                graph = shuffle_graph(graph, created_at)
                avg_degree =  calculate_avg_degree(graph)
                out_put.write(str(avg_degree)+"\n")
            except Exception as e:
                # this except block is here to handle the following sample limit lines
                # {"limit":{"track":19,"timestamp_ms":"1446218985758"}}
                pass
    out_put.close()
    input_file.close()
    
if __name__ == "__main__":
   main(sys.argv[1:])

