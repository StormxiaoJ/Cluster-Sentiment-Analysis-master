"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""

import tweepy
import couchdb
import json
from SentimentAnalysis.SentimentAnalysis import sentiment_polarity

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self,f_name='twitter.json',output2File=False, couch_user = 'admin',couch_password = 'admin',couch_host='127.0.0.1',couch_port=5984,db_name='test',raw_db_name='test', suburbs= None,api=None):
        tweepy.StreamListener(api)
        self.f_name=f_name
        self.output2File=output2File
        self.couch_user=couch_user
        self.couch_password=couch_password
        self.couch_host=couch_host
        self.couch_port=couch_port
        self.db_name=db_name
        self.raw_db_name = raw_db_name
        self.suburbs=suburbs

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            self.output2couchdb(data)
            if self.output2File:
                with open(self.f_name, 'a') as f:
                    f.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print("Error" + str(status))
        # if status == 420:
        #     # returning False in on_error disconnects the stream
        #     return False
        return True

    def output2couchdb(self,data):
        host_and_port = "http://" + self.couch_user + ":" + self.couch_password + "@" + self.couch_host + ":" + str(self.couch_port)
        couch = couchdb.Server(host_and_port)
        try:
            db = couch[self.db_name]  # existing
        except:
            db = couch.create(self.db_name)  # create db

        try:
            raw_db = couch[self.raw_db_name]  # existing
        except:
            raw_db = couch.create(self.raw_db_name)  # create db

        twitter = json.loads(data.encode('utf-8'))
        raw_db[twitter['id_str']] = twitter
        info = sentiment_polarity(twitter, self.suburbs)
        process_data = []
        if info != None:
            process_data.append(info)
        db.update(process_data)