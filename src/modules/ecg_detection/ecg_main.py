#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pathlib
import heartpy as hp
import os
import pandas as pd
from scipy.signal import savgol_filter, resample



def ecg_analysis(data):

    sample_rate = 50
    # wd, m = hp.process(unfiltered_ecg, sample_rate, windowsize=10)
    wd, m = hp.process_segmentwise(data, sample_rate, 10)
    print([round(x, 1) for x in m['bpm']])

    return [round(x, 1) for x in m['bpm']]

        # hp.plotter(wd, m)
        # plt.show()