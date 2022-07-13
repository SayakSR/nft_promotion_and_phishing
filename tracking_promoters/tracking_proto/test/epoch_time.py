# def convert_created_at(created_at):
 
#     import datetime
#     created_at = "2022-06-28T05:02:27.000Z"
#     datetime_stamp=datetime.datetime.strptime(created_at,"%Y-%m-%dT%H:%M:%S.%fZ")
#     return datetime_stamp

# def convert_to_epoch(datetime_stamp):
#      import datetime
#      epoch=datetime.datetime.strptime(datetime_stamp,"%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
#      return epoch



# def fetch_datestamp():

#     from datetime import datetime  
#     time_stamp = 1617295943.17321

#     dstamp = datetime.fromtimestamp(time_stamp)

#     return dstamp


# print(fetch_datestamp())

import time

date_time = '29.08.2011 11:05:02'
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
print(epoch)