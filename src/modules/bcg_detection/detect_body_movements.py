"""
Created on %(27/10/2016)
Function to detect bed patterns
"""

import math
import matplotlib
matplotlib.use('agg')
from matplotlib.pyplot import plot, savefig, figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

# The segmentation is performed based on the standard deviation of each time window
# In general if the std is less than 15, it means tha the there is no any pressure applied to the mat.
# if the std if above 2 * MAD all time-windows SD it means, we are facing body movements.
# On the other hand, if the std is between 15 and 2 * MAD of all time-windows SD,
# there will be a uniform pressure to the mat. Then, we can analyze the sleep patterns

def detect_patterns(pt1, pt2, win_size, data, time, plot):
    # store start and end time point
    pt1_ = pt1
    pt2_ = pt2

    limit = int(math.floor(data.size / win_size))
    flag = np.zeros([data.size, 1])
    event_flags = np.zeros([limit, 1])

    segments_sd = []

    for i in range(0, limit):
        sub_data = data[pt1:pt2]
        segments_sd.append(np.std(sub_data, ddof=1))
        pt1 = pt2
        pt2 += win_size

    mad = np.sum(np.abs(segments_sd - np.mean(segments_sd, axis=0))) / (1.0 * len(segments_sd))

    thresh1, thresh2 = 15, 2 * mad

    pt1, pt2 = pt1_, pt2_

    for j in range(0, limit):
        std_fos = np.around(segments_sd[j])
        if std_fos < thresh1:  # No-movement
            flag[pt1:pt2] = 3
            event_flags[j] = 3
        elif std_fos > thresh2:  # Movement
            flag[pt1:pt2] = 2
            event_flags[j] = 2
        else:
            flag[pt1:pt2] = 1  # Sleeping
            event_flags[j] = 1
        pt1 = pt2
        pt2 += win_size

    pt1, pt2 = pt1_, pt2_

    # Function to highlight activities
    data_for_plot = data
    width = np.min(data_for_plot)
    if width < 0:
        height = np.max(data_for_plot) + np.abs(width)
    else:
        height = np.max(data_for_plot)

    if plot == 1:
        # fig = plt.figure()
        current_axis = plt.gca()
        plt.plot(np.arange(0, data.size), data_for_plot, '-k', linewidth=1)
        plt.xlabel('Time [Samples]')
        plt.ylabel('Amplitude [mV]')
        plt.gcf().autofmt_xdate()

    for j in range(0, limit):
        sub_data = data_for_plot[pt1:pt2]
        sub_time = np.arange(pt1, pt2)/50
        if event_flags[j] == 3:  # No-movement
            if plot == 1:
                plt.plot(sub_time, sub_data, '-k', linewidth=1)
                current_axis.add_patch(
                    Rectangle((pt1, width), win_size, height, facecolor="#FAF0BE", alpha=.2))
        elif event_flags[j] == 2:  # Movement
            if plot == 1:
                plt.plot(sub_time, sub_data, '-k', linewidth=1)
                current_axis.add_patch(
                    Rectangle((pt1, width), win_size, height, facecolor="#FF004F", alpha=1.0))
        else:  # Sleeping
            if plot == 1:
                plt.plot(sub_time, sub_data, '-k', linewidth=1)
                current_axis.add_patch(
                    Rectangle((pt1, width), win_size, height, facecolor="#00FFFF", alpha=.2))
        pt1 = pt2
        pt2 += win_size

    plt.savefig('results/bcg_detection/rawData')

    # Remove Body Movements and bed-empty activities
    ind2remove = np.sort(np.append(np.where(event_flags == 3), np.where(event_flags == 2)), axis=None)
    mask = np.ones(data.size, dtype=bool)
    mask[ind2remove] = False
    filtered_data = data[mask]
    filtered_time = time[mask]

    return filtered_data, filtered_time