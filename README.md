## Challenge Summary

This challenge is to implement two features:

Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.

A tweet's text is considered "clean" once all of the escape characters (e.g. \n, \", \/ ) are replaced and unicode have been removed.


Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

A Twitter hashtag graph is a graph connecting all the hashtags that have been mentioned together in a single tweet.


## Running the Codebase Locally

1. git clone https://github.com/5ak3t/coding-challenge.git

2. Install requirements - `pip install -r requirements.txt`

3. Run Tests - `python src/tests.py` Test Fixtures are located in `coding-challenge/src/fixtures`

4. chmod +x coding-challenge/run.sh

5. ./run.sh

## Implementation Details

1. Common functions are written in `coding-challenge/src/utils.py`

2. Parsing of tweets is implemented in `coding-challenge/src/tweets_cleaned.py`

3. Calculating average degree is implemented in `coding-challenge/src/average_degree.py`

4. Cleaned tweets are written in `coding-challenge/src/tweet_output/ft1.txt`

5. Rolling average degree is written in `coding-challenge/src/tweet_output/ft2.txt`

## TODO Improvements For Future Versions

1. Proper Fixtures for Tests

2. Improve Test Coverage

3. Implement Threading

4. Run the code against live streaming API

5. The Graph creation and updation can have a better implementation.

6. Apache Spark can be used to ingest realtime data, GraphX for Grpah processing.
