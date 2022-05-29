from tempfile import TemporaryFile
import numpy as np
import pandas as pd
import requests
import json, requests, urllib, io
from io import StringIO
import csv
#import schedule
import time

import datetime
import os
from itertools import zip_longest
from pathlib import Path

# Global parameters utilized by both scan and report interfaces

global scan_url,URL_r,key,tc,params_scan,params_report,present

scan_url = 'https://www.virustotal.com/vtapi/v2/url/scan' # vtotal url where we scan URLs  
    
URL_r = 'https://www.virustotal.com/vtapi/v2/url/report'  # to get report.
key = 'aeaa9656525c9a1b99a3f8a4754457beb784b39e0aeb87ef24b6b79613d03339'
tc = -1 # initialize threatcount value to be -1 
   



def vt_scan(tweet_id,url):
    params_scan = {'apikey': key, 'url': url}  # parameters needed for vtotal API call. 
    # Scan the URL

    try:  
        resp = requests.post(scan_url, params = params_scan)
        print(resp.json())
        if(resp.status_code==200):
            print("URL sent for scan.")
        
    except ConnectionError as e:
        print(e)

def vt_report(tweet_id,url):

    params_report = {'apikey': key, 'resource': url}  # parameters needed for vtotal API call. 
    present = False

    try:
        resp = requests.get(URL_r, params=params_report)
        print("Report Retrived for {} with status code {}".format(url,resp.status_code))
        
        response = resp.json()  # getting the scan report.
        file=open("/home/sayaksr/Desktop/git/blockchain_codebase/output/log/vt/"+str(tweet_id)+".json","w")
        file.write(str(response))
        file.close()
        #print(response )
        # response will be in json format. 

    except Exception as e:
        print(e)

    # get the number of detections.
    try:
        tc = response['positives']  # get the detection number. 
        return tc
    except Exception as e:
        print(e)
