import datetime
import time

def fetch_date():

    date= datetime.datetime.today() 
    date=date.strftime("%m/%d/%Y, %H:%M:%S")
 
    return str(date)

def fetch_time(): # Epoch timestamp

    timestamp=time.time()

    return str(int(timestamp)) 


