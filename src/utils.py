#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module conatins common functions which are used for cleaning tweets, updating the graph,
extracting hashtags, and calculating the average degree.
"""
from __future__ import division
import re
import string
import codecs
import json
from htmlentitydefs import name2codepoint


def get_hashtag(text):
    """
    Input - single tweet text

    Output - All the hashtage

    The snippet has been adapted from the following URL - https://stackoverflow.com/questions/2527892/parsing-a-tweet-to-extract-hashtags-into-an-array-in-python
    """

    return set([re.sub(r"#+", "#", k) for k in set([re.sub(r"(\W+)$", "", j, flags=re.UNICODE) for j in set([i for i in text.split() if i.startswith("#")])])])


def unescape(s):
    """
    Input - single tweet text

    Output - unescape HTML code refs; c.f. http://wiki.python.org/moin/EscapingHtml

    """
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: unichr(name2codepoint[m.group(1)]), s)


def _clean_string(text):
    """
    Input - single tweet text

    Output - Returns a string which has unicode and escape characters removed.

    sample_text = "I'm at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa, PB https://t.co/HOl34REL1a",
    return_text = "I'm at Terminal de Integrao do Varadouro in Joo Pessoa, PB https://t.co/HOl34REL1a"

    """

    clean = text.encode("ascii", "ignore").decode("ascii") == text

    text = unescape(text)
    lst = list()
    for c in text:
        ord_c = ord(c)
        if ord_c < 128:
            # ignoring all ^chars like ^M ^R ^E
            if ord_c > 31:
                lst.append(c)
        else:
            try:
                lst.append('&%s;' % name2codepoint[ord_c])
            except KeyError:
                pass  # Charachter unknown
    return [clean, ''.join(lst)]


def update_or_build_graph(graph, hash_tags, created_at):
    """
    Input - existing/empty graph, Python Set of hash_tags found in a tweet text, the time of tweet creation.

    Output - Returns a weighted graph, the graph structure is explained below.

    Weight between the edge is the datetime object of the time when the tweet containing the hashtags was created.

    A sample graph represention is shown below :

    Apache <-> Spark <-> Storm <-> Hadoop <-> Spark

    Spark <-> Apache <-> HBase <-> Flink

    Storm <-> Apache <-> Hadoop

    Hadoop <-> Storm <-> Apache

    HBase <-> Spark

    Flink <-> Spark

    where datetime is the python object, fetched from the hashtag and is the weight of the edge
{
    "#Apache": {
    "#Storm": "datetime.datetime(2015, 10, 29, 17, 51, 30, tzinfo=tzutc())",
    "#Hadoop": "datetime.datetime(2015, 10, 29, 17, 52, 5, tzinfo=tzutc())",
    "#Spark": "datetime.datetime(2015, 10, 29, 17, 51, 1, tzinfo=tzutc())"
    },
    "#Spark": {
    "#Apache": "datetime.datetime(2015, 10, 29, 17, 51, 1, tzinfo=tzutc())",
    "#HBase": "datetime.datetime(2015, 10, 29, 17, 51, 59, tzinfo=tzutc())",
    "#Flink": "datetime.datetime(2015, 10, 29, 17, 51, 56, tzinfo=tzutc())"
    },
    "#Storm": {
    "#Apache": "datetime.datetime(2015, 10, 29, 17, 51, 30, tzinfo=tzutc())",
    "#Hadoop": "datetime.datetime(2015, 10, 29, 17, 51, 30, tzinfo=tzutc())"
    },
    "#Hadoop": {
    "#Storm": "datetime.datetime(2015, 10, 29, 17, 51, 30, tzinfo=tzutc())",
    "#Apache": "datetime.datetime(2015, 10, 29, 17, 52, 5, tzinfo=tzutc())"
    },
    "#HBase": {
    "#Spark": "datetime.datetime(2015, 10, 29, 17, 51, 59, tzinfo=tzutc())"
    },
    "#Flink": {
    "#Spark": "datetime.datetime(2015, 10, 29, 17, 51, 56, tzinfo=tzutc())"
    }
}


    """

    for single_hash in hash_tags:

        # update graph if number of hashtag is greater than one
        if len(hash_tags) > 1:
            for tag in hash_tags:
                if tag != single_hash:
                    if not graph.has_key(tag):
                        graph[tag] = dict()
                    graph[tag][single_hash] = created_at

    # remove edges that were created 60 seconds ago
    for top_k, top_v in graph.items():
        for k, v in top_v.items():
            diff = (created_at - v).seconds
            if diff >= 60:
                del graph[top_k][k]
                del graph[k][top_k]

    # remove nodes that do not have a value
    return dict({k: v for k, v in graph.items() if v})


def calculate_avg_degree(graph):
    """
    Input - Graph Object

    Output - Returns the average degree with precision of 2 digits.
    """
    sum = 0
    for tag in graph.keys():
        sum += len(graph[tag])
    div = float(sum) / len(graph)
    return round(div, 2)
