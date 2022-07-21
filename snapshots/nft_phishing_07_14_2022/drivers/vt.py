from virustotal_python import VirustotalError
from pprint import pprint
from base64 import urlsafe_b64encode
import hashlib

# Source - https://github.com/dbrennand/virustotal-python

from virustotal_python import Virustotal

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

def vt_scan_and_get_report(url_id,url,current_time):
    URL_ = 'https://www.virustotal.com/vtapi/v2/url/scan' # vtotal url where we scan URLs  
    URL_r = 'https://www.virustotal.com/vtapi/v2/url/report'  # to get report.
    key = 'aeaa9656525c9a1b99a3f8a4754457beb784b39e0aeb87ef24b6b79613d03339'
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
        
        response = resp.json()  # getting the scan report.
        file=open(f"vt_reports/{url_id}_{current_time}.json","w")
        file.write(str(response))
        file.close()

    except Exception as e:
        print(e)

    # get the number of detections.
    try:
        tc = response['positives']  # get the detection number. 
        return tc
    except Exception as e:
        print(e)
