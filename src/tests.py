#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
from dateutil import parser as dtparser
from utils import get_hashtag, _clean_string, update_or_build_graph, update_or_build_graph, calculate_avg_degree, shuffle_graph


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
FIXTURE_ONE_PATH =  os.path.join(FILE_PATH, "fixtures/fixture1.json")
FIXTURE_TWO_PATH =  os.path.join(FILE_PATH, "fixtures/fixture2.json")

class FeatureOneTestCase(unittest.TestCase):

    def setUp(self):
        with open(FIXTURE_ONE_PATH) as fixture:
            for line in fixture:
                json_line = json.loads(line)
                self.test_tweet_text = json_line['text']
                self.test_tweet_created = json_line['created_at']
            self.correct_unicode_tweet = "#Spark #Apache I'm at Terminal de Integrao do Varadouro in Joo Pessoa, PB https://t.co/HOl34REL1a"

    def tearDown(self):
        self.unicode_tweet = None
        self.hashtag_tweet = None

    def test_hashtag_count(self):
        hashtags = get_hashtag(self.test_tweet_text)
        self.assertEqual(len(hashtags), 2, 'incorrect hashtags')

    def test_tweet_cleaning_and_formatting(self):

        clean, cleaned_tweet = _clean_string(self.test_tweet_text)
        self.assertEqual(
            clean, False, "incorrect testing of unicode and escape character presence")
        self.assertEqual(cleaned_tweet, self.correct_unicode_tweet,
                         "incorrect escaping and formatting of tweet")


class FeatureTwoTestCase(unittest.TestCase):

    def setUp(self):
        with open(FIXTURE_TWO_PATH) as fixture:
            self.tweet_list = []
            for line in fixture:
                self.tweet_list.append(json.loads(line))
            self.graph = {}
            self.avg_degree_list = []

    def tearDown(self):
        self.tweet_list = []
        self.graph = {}
        self.avg_degree_list = []

    def test_rolling_avg_degree(self):

        for tweet in self.tweet_list:
            created_at = dtparser.parse(tweet["created_at"])
            clean, cleaned_line = _clean_string(tweet['text'])
            hash_tags = get_hashtag(cleaned_line)
            if hash_tags:
                self.graph = update_or_build_graph(
                    self.graph, hash_tags, created_at)
                # print self.graph
            self.graph = shuffle_graph(self.graph, created_at)
            self.avg_degree_list.append(calculate_avg_degree(self.graph))
        #print self.avg_degree_list
        self.assertEqual(self.avg_degree_list, [1.0, 2.0, 2.0, 2.0, 1.67],
                         'incorrect average degree')

if __name__ == '__main__':
    unittest.main()
