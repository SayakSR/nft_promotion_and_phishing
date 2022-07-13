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

def convert_created_at(created_at): # Function to convert twitter created_at to python timestamp
 
    import datetime
    datetime_stamp=datetime.datetime.strptime(created_at,"%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime_stamp

def convert_to_epoch(datetime_stamp): # Function to convert python timestamp to unix timestamp
     import datetime
     epoch=datetime.datetime.strptime(datetime_stamp,"%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
     return epoch

def datetime_to_epoch(input): # Epoch timestamp

    input=str(input)
    import datetime
    epoch=datetime.datetime.strptime(input,"%Y-%m-%d %H:%M:%S").timestamp()
    return epoch