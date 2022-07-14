from drivers.date_time_stamp import *
import os
import time

timestamp=fetch_time()

timestamp=timestamp+7200
timestamp=timestamp-600

date=convert_epoch_to_datetime(timestamp)
print(date)

os.system(f'twarc2 timeline --use-search --start-time "{date}"  --limit 10 --exclude-retweets --exclude-replies sayaksaharoy p.json')
