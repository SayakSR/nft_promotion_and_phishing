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

def vt_scan_and_get_report(url,url_id,timestamp):

    URL_ = 'https://www.virustotal.com/vtapi/v2/url/scan' # vtotal url where we scan URLs  
    URL_r = 'https://www.virustotal.com/vtapi/v2/url/report'  # to get report.
    key = 'd80137e9f5e82896483095b49a7f0e73b5fd0dbc7bd98f1d418ff3ae9c83951e'
    tc = -1 # initialize threatcount value to be -1 
   
    params = {'apikey': key, 'resource': url}  # parameters needed for vtotal API call. 
    present = False


    # scan the URL first. 

    try:  
        resp = requests.get(URL_, params = params)
        if(resp.status_code==200):
            print("URL sent for scan.")
        
    except ConnectionError as e:
        print(e)
    
    try:
        resp = requests.get(URL_r, params=params)
        print("Report Retrived for {} with status code {}".format(url,resp.status_code))
        print(resp)
        response = resp.json()  # getting the scan report.
        # file=open("raw/"+str(url_id)+"_"+str(timestamp)+".txt","w")
        # file.write(str(response))
        # file.close()
        print(response )
        # response will be in json format. 

    except Exception as e:
        print(e)

    # get the number of detections.
    try:
        tc = response['positives']  # get the detection number. 
        return tc
    except Exception as e:
        print(e)

vt_scan_and_get_report("http://moonbirds2022.com",12345,45678)
