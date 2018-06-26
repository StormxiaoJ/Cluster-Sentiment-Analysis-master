"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""

import requests
import json

auth=('admin','admin')

def get_geocoded_tweets(url, start_key,end_key,include_docs='false',reduce='true',group_level='1',skip='0',limit=None,auth=('admin','admin')):
    if limit==None:
        payload = {'include_docs': include_docs,'group_level':group_level, 'reduce': reduce, 'skip': skip,'start_key':start_key,'end_key':end_key}  # without limit
    else:
        payload = {'include_docs': include_docs,'group_level':group_level, 'reduce': reduce, 'skip': skip,'limit':limit,'start_key':start_key,'end_key':end_key}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)

    try:
        return r.json()
    except:
        print(r.status_code)
        exit(-1)

data=get_geocoded_tweets('http://115.146.86.168:5984/processed_twitter/_design/tweets_analysis/_view/suburb_day_drunk','Hawthorn','Melbourne')
print(data)