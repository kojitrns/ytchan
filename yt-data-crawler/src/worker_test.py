# coding: utf-8
import sys
import time
from datetime import datetime

with open('workerlog', mode='w') as f:
	while 0<1:
		f.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S\n"))
		f.flush()
		time.sleep(5)