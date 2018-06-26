"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""
import tweepy
import couchdb
import sys, getopt
import json
from SentimentAnalysis.SentimentAnalysis import sentiment_polarity
from MyStreamListener import MyStreamListener

def get_authorization(access_file):
    with open(access_file) as f:
        access_str = f.read()

    access = json.loads(access_str)

    info = {"consumer_key": access['CONSUMER_KEY'],
            "consumer_secret": access['CONSUMER_SECRET'],
            "access_token": access['ACCESS_TOKEN'],
            "access_secret": access['ACCESS_TOKEN_SECRET']}

    auth = tweepy.OAuthHandler(info['consumer_key'], info['consumer_secret'])
    auth.set_access_token(info['access_token'], info['access_secret'])
    return auth

def get_tweets(db_json,access_json,grid_json,circle):
    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    with open(grid_json) as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)


    couch_user = db_info['user']
    couch_password = db_info['password']
    couch_host = db_info['host']
    couch_port = db_info['port']
    db_name = db_info['processed_database']
    raw_db_name = db_info['raw_database']
    # source_url = db_info['tweet_source']
    host_and_port = "http://" + couch_user + ":" + couch_password + "@" + couch_host + ":" + str(couch_port)

    couch = couchdb.Server(host_and_port)
    try:
        db = couch[db_name]  # existing
    except:
        db = couch.create(db_name)  # create db

    try:
        raw_db = couch[raw_db_name]  # existing
    except:
        raw_db = couch.create(raw_db_name)  # create db


    api = tweepy.API(get_authorization(access_json),wait_on_rate_limit=True)
    for status in tweepy.Cursor(api.search,q='',geocode=circle).items():
        # data = status._json
        twitter = status._json
        raw_db[twitter['id_str']] = twitter
        info = sentiment_polarity(twitter, suburbs)
        process_data = []
        if info != None:
            process_data.append(info)
        db.update(process_data)

def create_stream(locations, access_json ,db_json, grid_json, f_name=None):
    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    with open(grid_json) as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)

    listener = MyStreamListener(f_name=f_name,couch_user = db_info['user'],couch_password = db_info['password'], couch_host=db_info['host'], couch_port=db_info['port'], db_name=db_info['processed_database'],raw_db_name=db_info['raw_database'],suburbs=suburbs)
    stream = tweepy.Stream(get_authorization(access_json), listener)
    stream.filter(locations=locations)


def main(argv):
    # West Australia
    wa_location = [112.8,-35.33,129,-13.5]
    # Northern Territory
    nt_location = [129,-26,138,-10.75]
    # South Australia
    sa_location = [129,-38.1,141,-26]
    # Queensland, NSW, Victoria, Tasmania
    qnvt_location = [138,-26,141,-15.8, 141,-15.8,146,-10.5, 141,-43.8,154,-15.8]

    location0= '-37.815,144.9622,450km'
    location1 = '-35.828,143.03,300km'
    location2 = '-37.223,147.117,350km'
    location3 = '-37.537,143.03,300km'

    outputfile = 'twitter.json'
    access_token_json = 'access0.json'
    db_json = 'db.json'
    grid_json ='vic.json'
    location = qnvt_location
    circle = location3
    search = False
    try:
        opts, args = getopt.getopt(argv, "ho:a:d:l:g:s:", ["outputfile=",'access=','database=','location=','grid=','search='])
    except getopt.GetoptError:
        print ("""-o <output_filename>
                  -a <access_token_josn>
                  -d <database_json>
                  -s <search history: 1>
                  -l < West Australia: 3,
                               Northern Territory: 2,
                               South Australia: 1
                               Queensland, NSW, Victoria, Tasmania: 0""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-o <output_filename>
                      -a <access_token_josn>
                      -d <database_json>
                      -s <search history: 1>                          
                      -l < West Australia: 3,
                               Northern Territory: 2,
                               South Australia: 1
                               Queensland, NSW, Victoria, Tasmania: 0""")
            sys.exit()
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-a", "--access"):
            access_token_json = arg
        elif opt in ("-d", "--database"):
            db_json = arg
        elif opt in ("-s", "--search"):
            if arg == '1':
                search = True
        elif opt in ("-l", "--location"):
            if arg == '3':
                circle = location3
                location = wa_location
            elif arg == '2':
                circle = location2
                location = nt_location
            elif arg == '1':
                circle = location1
                location = sa_location
            elif arg == '0':
                circle = location0
                location = qnvt_location
            else:
                print ("""-l < West Australia: 3,
                               Northern Territory: 2,
                               South Australia: 1
                               Queensland, NSW, Victoria, Tasmania: 0""")
                sys.exit(2)
        elif opt in ("-g", "--grid"):
            grid_json = arg

    if search:
        get_tweets(db_json, access_token_json, grid_json, circle)
    else:
        create_stream(location, access_token_json,db_json,grid_json,f_name=outputfile,)


if __name__ == "__main__":
   main(sys.argv[1:])