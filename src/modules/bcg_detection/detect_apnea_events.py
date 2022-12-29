"""
Created on %(25/09/2017)
Function to detect apnea events.
It returns the start and end time of each detected apnea event
"""

import math

import numpy as np
import pandas as pd


def unix_time_converter(unix_time):
    tm = pd.to_datetime(unix_time, unit='ms')
    readable_time = tm.tz_localize('UTC').tz_convert('Asia/Singapore').strftime("%H.%M.%S")
    return readable_time


def apnea_events(data, utc_time, thresh):
    pt1, pt2, win_size = 0, 1500, 1500
    hop_size, win_shift = 500, win_size
    limit = int(math.floor(data.size / win_size))
    counter = 0
    start_time, stop_time, apnea_events = [], [], {}
    for i in range(0, limit):

        StDs = []
        sub_data = data[pt1:pt2]
        sub_utc_time = utc_time[pt1:pt2]
        sub_sub_utc_time = []

        for so in range(0, win_shift, hop_size):
            ndx = np.arange(so, so + hop_size)
            sub_sub_utc_time.append(sub_utc_time[ndx])
            fiber_optic_data = sub_data[ndx]

            StDs.append(np.std(fiber_optic_data, ddof=1))

        T = np.mean(StDs)

        ind = [i for i, v in enumerate(StDs) if v <= thresh * T]

        if ind:
            for j in ind:
                counter += 1
                current_time = sub_sub_utc_time[j]
                start_time.append(unix_time_converter(current_time[0]))
                stop_time.append(unix_time_converter(current_time[-1]))
                print('\nApnea Information')
                print('start time : ', start_time, ' stop time : ', stop_time)

        pt1 = pt2
        pt2 += win_size

    apnea_events[0] = start_time
    apnea_events[1] = stop_time
    return apnea_events
