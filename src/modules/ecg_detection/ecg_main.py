#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import heartpy as hp
import os
import pandas as pd
from scipy.signal import savgol_filter, resample
from modules.bcg_detection.modwt_matlab_fft import modwt
from modules.bcg_detection.modwt_mra_matlab_fft import modwtmra



def ecg_analysis(data):

    sample_rate = 50

    w = modwt(data, 'bior3.9', 4)
    dc = modwtmra(w, 'bior3.9')
    wavelet_cycle = dc[4]

    # limit = int(math.floor(data.size / 500))
    # t1, t2, window_length, window_shift = 0, 500, 500, 500

    # all_rate = []
    # for j in range(0, limit):
    #     sub_signal = wavelet_cycle[t1:t2]
    #     if j == 23: print(np.mean(sub_signal))
    #     wd, m = hp.process(sub_signal, sample_rate)
    #     if np.isnan(m['bpm']): all_rate.append(all_rate[-1])
    #     else: all_rate.append(round(m['bpm'], 1))
    #     t1 = t2
    #     t2 += window_shift
    # # all_rate = np.vstack(all_rate).flatten()

    # # print(all_rate)
    # return all_rate

    wd, m = hp.process_segmentwise(wavelet_cycle, sample_rate, 10)
    # print([round(x, 1) for x in m['bpm']])

    return [round(x, 1) for x in m['bpm']]

        # hp.plotter(wd, m)
        # plt.show()