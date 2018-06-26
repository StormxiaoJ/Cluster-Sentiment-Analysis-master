"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""

from textblob import TextBlob
import couchdb
import json
from geojson_utils import point_in_polygon
from nltk.tokenize import TweetTokenizer
import sys
import getopt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

def sentiment_polarity(twitter_data,suburbs):
    analyzer = SentimentIntensityAnalyzer()
    twitter = twitter_data
    s = None
    if not twitter['coordinates'] == None:
        for suburb in suburbs:
            if point_in_polygon(twitter['coordinates'], suburb['geometry']):
                s = suburb['properties']['Suburb_Name']
                break

        if s != None:
            try:
                text = twitter['extended_tweet']['full_text']
            except:
                text = twitter['text']

            if not twitter['lang'] == 'en':  # If the language is not English, translate it.
                try:
                    blob = TextBlob(text)
                    blob = blob.translate(from_lang=twitter['lang'], to="en")
                    text = blob.raw
                except:
                    return None # If the twitter cannot be translated, let go.

            analysis_data = dict()
            analysis_data['_id'] = twitter['id_str']
            analysis_data['suburb'] = s
            analysis_data['hashtags'] = [ht['text'] for ht in twitter['entities']['hashtags']]
            analysis_data['polarity'] = analyzer.polarity_scores(text)['compound']
            analysis_data['drunk'] = drunk_filter(text)
            analysis_data['created_at'] = twitter['created_at'][:3]
            return analysis_data

    return None

def drunk_filter(text):
    regexps = [
    re.compile(r'\bshit\s*faced\b', re.IGNORECASE),
    re.compile(r'\bkeg\s*beer\b', re.IGNORECASE),
    re.compile(r'\bturn\s*up\b', re.IGNORECASE),
    re.compile(r'\bturnt\s*up\b', re.IGNORECASE),
    re.compile(r'\blit\s*up\b', re.IGNORECASE),
    re.compile(r'\bpoo\s*pooed\b', re.IGNORECASE),
    re.compile(r'\bpoo-?pooed\b', re.IGNORECASE),
    re.compile(r'\bbar\s*hop\b', re.IGNORECASE),
    re.compile(r'\bbeer\s*goggles\b', re.IGNORECASE),
    re.compile(r'\btoes?\s*up\b', re.IGNORECASE),
    re.compile(r'\bboot\s*and\s*rally\b', re.IGNORECASE),
    re.compile(r'\bbeer\s*pong\b', re.IGNORECASE),
    re.compile(r'\bbeer\s*belly\b', re.IGNORECASE),
    re.compile(r'\bflip\s*cup\b', re.IGNORECASE),
    re.compile(r'\bbud\s*light\b', re.IGNORECASE),
    re.compile(r'\bnight\s*club\b', re.IGNORECASE),
    re.compile(r'\bdrinking\s*games?\b', re.IGNORECASE),
    re.compile(r'\bshit-?faced\b', re.IGNORECASE),
    re.compile(r'\bfucked\s+up\b', re.IGNORECASE),
    re.compile(r'\bdrunk\b', re.IGNORECASE),
    re.compile(r'\balcohol\b', re.IGNORECASE),
    re.compile(r'\bparty\b', re.IGNORECASE),
    re.compile(r'\bbooze\b', re.IGNORECASE),
    re.compile(r'\bliquor\b', re.IGNORECASE),
    re.compile(r'\bvodka\b', re.IGNORECASE),
    re.compile(r'\bhangover\b', re.IGNORECASE),
    re.compile(r'\bwasted\b', re.IGNORECASE),
    re.compile(r'\btequila\b', re.IGNORECASE),
    re.compile(r'\bcocktail\b', re.IGNORECASE),
    re.compile(r'\bwhiske?y\b', re.IGNORECASE),
    re.compile(r'\bscotch\b', re.IGNORECASE),
    re.compile(r'\brum\b', re.IGNORECASE),
    re.compile(r'\bplastered\b', re.IGNORECASE),
    re.compile(r'\bsloshed\b', re.IGNORECASE),
    re.compile(r'\bhammered\b', re.IGNORECASE),
    re.compile(r'\btrashed\b', re.IGNORECASE),
    re.compile(r'\btipsy\b', re.IGNORECASE),
    re.compile(r'\bbuzzed\b', re.IGNORECASE),
    re.compile(r'\bbeer\b', re.IGNORECASE),
    re.compile(r'\bshot\b', re.IGNORECASE),
    re.compile(r'\bbrew\b', re.IGNORECASE),
    re.compile(r'\bwine\b', re.IGNORECASE),
    re.compile(r'\bbar\b', re.IGNORECASE),
    re.compile(r'\bchampagne\b', re.IGNORECASE),
    re.compile(r'\blager\b', re.IGNORECASE),
    re.compile(r'\bclub\b', re.IGNORECASE),
    re.compile(r'\bpub\b', re.IGNORECASE),
    re.compile(r'\balcoholic\b', re.IGNORECASE),
    re.compile(r'\bbottles?\b', re.IGNORECASE),
    re.compile(r'\bcrown\b', re.IGNORECASE),
    re.compile(r'\bbinge\b', re.IGNORECASE),
    re.compile(r'\bboozy\b', re.IGNORECASE),
    re.compile(r'\blean\b', re.IGNORECASE),
    re.compile(r'\bhennessy\b', re.IGNORECASE),
    re.compile(r'\bHenee\b', re.IGNORECASE),
    re.compile(r'\bkegger\b', re.IGNORECASE),
    re.compile(r'\bciroc\b', re.IGNORECASE),
    re.compile(r'\bcognac\b', re.IGNORECASE),
    re.compile(r'\byac\b', re.IGNORECASE),
    re.compile(r'\byak\b', re.IGNORECASE),
    re.compile(r'\bhammed\b', re.IGNORECASE)
    ]
    for pattern in regexps:
        match = pattern.search(text)
        if bool(match):
            return 1
    return 0



