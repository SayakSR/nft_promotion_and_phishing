from promotee_tracker import *
from promotee_followers import *
from drivers.countdown import countdown
import time

# Runs every 1 hour
while 1:
   run_promotee_followers_main()
   countdown(3600)


