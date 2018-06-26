"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""
from flask import Flask, render_template,request,jsonify
import requests
import urllib.request
import json


def get_geocoded_tweets(url, group_level,include_docs='false',reduce='true',skip='0',limit=None,auth=('admin','admin')):
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


app = Flask(__name__)



@app.route('/',methods=['GET'])
def home():
    return render_template('map.html')


@app.route('/table',methods=['GET'])
@app.route('/table/<name>')
def table(name=None):
    return render_template('table.html',name=name)

@app.route('/drunk',methods=['POST'])
def drunk():
    request_data= request.get_json(force=True)
    data_drunk = get_geocoded_tweets('http://115.146.86.168:5984/processed_twitter/_design/tweets_analysis/_view/suburb_day_drunk',2)
    data_polarity = get_geocoded_tweets('http://115.146.86.168:5984/processed_twitter/_design/tweets_analysis/_view/suburb_day_polarity', 2)
    returnDrunk = {}
    returnPolarity = {}

    with open('day_drunk.json','w')as f:
        json.dump(data_drunk,f)
    with open('day_polarity.json','w')as fp:
        json.dump(data_polarity,fp)

    for row in data_drunk['rows']:
        if(row['key'][0].rstrip() == request_data['stateName'].rstrip()):
            returnDrunk[row['key'][1]] = row['value']
    for row in data_polarity['rows']:
        if(row['key'][0].rstrip() == request_data['stateName'].rstrip()):
            returnPolarity[row['key'][1]] = row['value']
    return jsonify(dataPolarity=returnPolarity,dataDrunk=returnDrunk)

@app.route('/sentiment',methods=['GET'])
def sentiment():
    data = get_geocoded_tweets('http://115.146.86.168:5984/processed_twitter/_design/tweets_analysis/_view/suburb_polarity',1)
    with open('suburb_polarity.json','w')as f:
        json.dump(data,f)
    return jsonify(name='data',data=data)

@app.route('/wordCloud',methods=['POST'])
def wordCloud():
    request_data = request.get_json(force=True)
    data = get_geocoded_tweets('http://115.146.86.168:5984/processed_twitter/_design/tweets_analysis/_view/suburb_hash',2)
    returnData = {}
    with open('wordCloud.json','w') as f:
        json.dump(data,f)
    for row in data['rows']:
        if(row['key'][0].rstrip() == request_data['stateName'].rstrip()):
            returnData[row['key'][1]] = row['value']
    return jsonify(name='data',data=returnData)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)