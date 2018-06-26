"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""

import requests
import couchdb
import json
import sys
import getopt



auth=('admin','admin')

def get_geocoded_tweets(url, include_docs='false',reduce='true',group_level='1',skip='0',limit=None,auth=('admin','admin')):
    if limit==None:
        payload = {'include_docs': include_docs,'group_level':group_level, 'reduce': reduce, 'skip': skip}  # without limit
    else:
        payload = {'include_docs': include_docs,'group_level':group_level, 'reduce': reduce, 'skip': skip,'limit':limit}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)

    try:
        return r.json()
    except:
        print(r.status_code)
        exit(-1)

def put_data_into_couchdb(db_json,grid_json,start,end):

    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    couch_user = db_info['user']
    couch_password = db_info['password']
    couch_host = db_info['host']
    couch_port = db_info['port']
    db_name = db_info['processed_database']
    raw_db_name = db_info['raw_database']
    source_url = db_info['tweet_source']
    host_and_port = "http://" +couch_user+":"+couch_password+"@"+couch_host + ":" + str(couch_port)

    couch = couchdb.Server(host_and_port)
    try:
        db = couch.create(db_name)  # create db
    except:
        db = couch[db_name]  # existing

    try:
        raw_db = couch[raw_db_name]  # existing
    except:
        raw_db = couch.create(raw_db_name)  # create db


    with open(grid_json) as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)

    total_rows = get_geocoded_tweets(source_url,start_key=start,end_key=end, skip=0, limit=1, auth=auth)['total_rows']



    limit = 100
    for i in range(int(total_rows/limit)):
        skip=str(i*limit)
        try:
            geocoded_tweets = get_geocoded_tweets(source_url, start_key=start, end_key=end, skip=skip, limit=limit,
                                                  auth=auth)
            print (len(geocoded_tweets['rows']))
            process_data = []
            raw_data = []
            for tweet in geocoded_tweets['rows']:
                twitter = tweet['doc']
                twitter.pop('_rev')
                raw_data.append(twitter)
                info = sentiment_polarity(twitter, suburbs)
                if info != None:
                    process_data.append(info)
            raw_db.update(raw_data)
            db.update(process_data)
        except:
            pass

    try:
        geocoded_tweets = get_geocoded_tweets(source_url, start_key=start, end_key=end, skip=skip, auth=auth)
        process_data = []
        raw_data = []
        for tweet in geocoded_tweets['rows']:
            twitter = tweet['doc']
            # Remove _rev so the data can be stored in couchdb
            twitter.pop('_rev')
            raw_data.append(twitter)
            info = sentiment_polarity(twitter, suburbs)
            if info != None:
                process_data.append(info)
        raw_db.update(raw_data)
        db.update(process_data)
    except:
        pass




def main(argv):
    db_json = 'db.json'
    grid_json = 'vic.json'
    start = 'r1h'
    end = 'r1r'
    try:
        opts, args = getopt.getopt(argv, "hs:e:d:g:", ['database=',"grid="])
    except getopt.GetoptError:
        print ("""-d <database_json>""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-d <database_json>""")
            sys.exit()
        elif opt in ("-s", "--start_geohash"):
            start = arg
        elif opt in ("-e", "--end_geohash"):
            end = arg
        elif opt in ("-d", "--database"):
            db_json = arg
        elif opt in ("-g", "--grid"):
            grid_json = arg

    start = '[\"'+start+'\"]'
    end = '[\"' + end + '\"]'
    put_data_into_couchdb(db_json,grid_json,start,end)


if __name__ == "__main__":
   main(sys.argv[1:])