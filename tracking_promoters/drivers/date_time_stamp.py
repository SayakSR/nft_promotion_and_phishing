import datetime
import time

def fetch_date():

    date= datetime.datetime.today() 
    date=date.strftime('%m/%d/%Y')
 
    return str(date)

def fetch_time(): # Epoch timestamp

    timestamp=time.time()

    return str(int(timestamp)) 


def fetch_datestamp():

    from datetime import datetime  
    time_stamp = 1617295943.17321

    dstamp = datetime.fromtimestamp(time_stamp)

    return dstamp

