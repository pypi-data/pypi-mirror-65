#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:08:09 2019

@author: crumpf
DrCRumpf@gmail.com
"""


import sys
import datetime
import time
import numpy as np


def ProgressStatus(i_operation, n_operations, datetime_t0):
    progress_percent = (float(i_operation+1)/float(n_operations))*100
    current_time = datetime.datetime.now()
    t_duration = current_time - datetime_t0
    second_per_percent = t_duration.total_seconds() / progress_percent
    second_remaining = (100.0 - progress_percent) * second_per_percent
    
    finish_time = current_time + datetime.timedelta(seconds=second_remaining)
    cout_string  = '{0:.1f}% done...projected finish on {1:s}'.format(progress_percent, finish_time.strftime('%y/%m/%d - %H:%M:%S'))
    sys.stdout.write('\r'+cout_string)
    if progress_percent == 100.0:
    	print('')
    



